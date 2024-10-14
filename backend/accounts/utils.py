from requests import (
    post, get, put, patch, delete, options, head, request,
    exceptions as requests_exceptions
)
from random import ( randint, )
from accounts.models import ( User, OneTimePassword, )
from django.core.mail import ( EmailMessage, )
from django.conf import ( settings, )
from rest_framework.exceptions import ( AuthenticationFailed, )
from google.auth.transport import ( requests as google_requests, )
from google.oauth2 import ( id_token, )
from django.contrib.auth import ( authenticate, )

# Generate a 6-digit OTP
def generateOTP():
    otp = ""
    for i in range(6):
        otp += str(randint(0, 9))
    return otp

# Send an OTP to the user's email for verification
def send_OTP_to_user(email):
    Subject = "One Time Passcode for Email Verification"
    otp_code = generateOTP()  # Generate a new OTP
    user = User.objects.get(email=email)  # Get the user by their email
    current_site = "nekon.net"
    email_body = f"Hello {user.first_name}, thanks for signing up with {current_site}. Please use the following one time passcode to verify your email address: {otp_code}"
    from_email = settings.DEFAULT_FROM_EMAIL

    # Store the OTP code in the OneTimePassword model
    OneTimePassword.objects.create(user=user, code=otp_code)

    # Send an email to the user with the OTP code
    send_mail = EmailMessage(subject=Subject, body=email_body, from_email=from_email, to=[email])
    send_mail.send(fail_silently=True)

# Send a regular email (not OTP-based)
def send_normal_email(data):
    email = EmailMessage(
        subject=data['email_subject'],
        body=data['email_body'],
        from_email=settings.EMAIL_HOST_USER,
        to=[data['to_email']]
    )
    email.send()

# GitHub OAuth utility class
class Github():
    @staticmethod
    # Exchange OAuth code for access token
    def exchange_code_for_token(code):
        params_payload = {
            "client_id": settings.GITHUB_CLIENT_ID,
            "client_secret": settings.GITHUB_CLIENT_SECRET,
            "code": code
        }
        # Make a POST request to GitHub's OAuth API to get the access token
        get_access_token = post(
            "https://github.com/login/oauth/access_token",
            params=params_payload,
            headers={'Accept': 'application/json'}
        )
        payload = get_access_token.json()  # Parse the JSON response
        token = payload.get('access_token')  # Extract the access token
        return token

    @staticmethod
    # Fetch GitHub user information using the access token
    def get_github_user(access_token):
        try:
            headers = {'Authorization': f'Bearer {access_token}'}
            resp = get('https://api.github.com/user', headers=headers)
            resp.raise_for_status()  # Raise error for HTTP 4xx/5xx responses
            user_data = resp.json()  # Parse the user data
            return user_data
        except requests_exceptions.HTTPError as e:
            raise AuthenticationFailed(f"HTTP Error: {str(e)}", 401)
        except requests_exceptions.ConnectionError as e:
            raise AuthenticationFailed("Failed to connect to GitHub", 503)
        except requests_exceptions.Timeout as e:
            raise AuthenticationFailed("Request timed out", 504)
        except requests_exceptions.RequestException as e:
            raise AuthenticationFailed(f"Request failed: {str(e)}", 500)
        except ValueError as e:
            # Handle JSON parsing errors
            raise AuthenticationFailed("Invalid response format", 500)

# Google OAuth utility class                        
class Google():
    @staticmethod
    # Validate Google OAuth access token
    def validate(access_token):
        try:
            id_info = id_token.verify_oauth2_token(
                access_token,
                google_requests.Request()
            )
            # Ensure the token is from Google Accounts
            if 'accounts.google.com' in id_info['iss']:
                return id_info
            else:
                raise AuthenticationFailed("Invalid issuer", 401)
        except ValueError as e:
            raise AuthenticationFailed("Invalid token format", 401)
        except Exception as e:
            raise AuthenticationFailed("The token is either invalid or has expired", 401)

def login_social_user(email, password):
    user=authenticate(email=email, password=password)
    user_tokens=user.tokens()
    return {
        'email': user.email,
        'full_name': user.get_full_name,
        'access_token': str(user_tokens.get('access')),
        'refresh_token': str(user_tokens.get('refresh'))
    }

# Register or authenticate a user using social login (GitHub or Google)
def register_social_user(provider, email, first_name, last_name):
    user=User.objects.filter(email=email)
    if user.exists():
        if provider == user[0].auth_provider:
            login_social_user(email, settings.SOCIAL_AUTH_PASSWORD)
        else:
            raise AuthenticationFailed(
                detail=f"Please continue your login using {user[0].auth_provider}"
            )
    else:
        new_user={
            'email': email,
            'first_name': first_name,
            'last_name': last_name,
            'password': settings.SOCIAL_AUTH_PASSWORD
        }
        register_user=User.objects.create_user(**new_user)
        register_user.auth_provider=provider
        register_user.is_verified=True
        register_user.save()
        login_social_user(email=register_user.email, password=settings.SOCIAL_AUTH_PASSWORD)
    

