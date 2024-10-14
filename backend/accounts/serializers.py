from accounts.models import ( User, )
from accounts.utils import ( send_normal_email, Google, Github, register_social_user, )
from django.conf import ( settings, )
from django.urls import ( reverse, )
from django.contrib.auth import ( authenticate, )
from django.utils.encoding import ( force_str, smart_bytes, )
from django.contrib.sites.shortcuts import ( get_current_site, )
from django.contrib.auth.tokens import ( PasswordResetTokenGenerator, )
from django.utils.http import ( urlsafe_base64_encode, urlsafe_base64_decode, )
from rest_framework import ( serializers, )
from rest_framework_simplejwt.tokens import ( RefreshToken, )
from rest_framework_simplejwt.exceptions import ( TokenError, )
from rest_framework.exceptions import ( AuthenticationFailed, )
# Create your serializers here.
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    confirm_password = serializers.CharField(max_length=68, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'first_name','last_name', 'password', 'confirm_password']

    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')
        if password != confirm_password:
            raise serializers.ValidationError({"password": "Passwords do not match"})
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password']
        )
        return user

class LoginSerializer(serializers.ModelSerializer):
    email=serializers.EmailField(max_length=255, min_length=6)
    password=serializers.CharField(max_length=68, write_only=True)
    full_name=serializers.CharField(max_length=255, read_only=True)
    access_token=serializers.CharField(max_length=255, read_only=True)
    refresh_token=serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model=User
        fields=['email', 'password', 'full_name', 'access_token', 'refresh_token']

    def validate(self, attrs):
        email=attrs.get('email')
        password=attrs.get('password')
        request=self.context.get('request')
        user=authenticate(request, email=email, password=password)
        if not user:
            raise AuthenticationFailed("Invalid credentials, try again")
        user_tokens = user.tokens()
        return {
                'email': user.email,
                'full_name': user.get_full_name,
                'access_token': user_tokens.get('access'),
                'refresh_token': user_tokens.get('refresh')
        }

class PasswordResetRequestSerializer(serializers.Serializer):
    email=serializers.EmailField(max_length=255)
    class Meta:
        fields=['email']
    def validate(self, attrs):
        email=attrs.get('email')
        if User.objects.filter(email=email).exists():
            user=User.objects.get(email=email)
            uidb64=urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            request = self.context.get('request')
            current_site=get_current_site(request=request).domain
            relative_link=reverse("password-reset-confirm", kwargs={'uidb64': uidb64, 'token': token})
            absurl=f"http://{current_site}{relative_link}"
            email_body = f"Hello, please use the link below to reset your password. \n {absurl}"
            data={
                'email_body': email_body,
                'email_subject': 'Reset your password',
                'to_email': user.email,
            }
            send_normal_email(data)
        return super().validate(attrs)

class SetNewPasswordSerializer(serializers.Serializer):
    password=serializers.CharField(max_length=68, min_length=6, write_only=True)
    confirm_password=serializers.CharField(max_length=68, min_length=6, write_only=True)
    uidb64=serializers.CharField(write_only=True)
    token=serializers.CharField(write_only=True)

    class Meta:
        fields=["password", "confirm_password", "uidb64", "token"]

    def validate(self, attrs):
        try:
            token=attrs.get('token')
            uidb64=attrs.get('uidb64')
            password=attrs.get('password')
            confirm_password=attrs.get('confirm_password')

            user_id = force_str(urlsafe_base64_decode(uidb64))
            user=User.objects.get(id=user_id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed("Reset Link is invalid or has expired.", 401)
            if password != confirm_password:
                raise AuthenticationFailed("Passwords do not match")
            user.set_password(password)
            user.save()
            return user
        except Exception as e:
            raise AuthenticationFailed("Reset Link is invalid or has expired.", 401)


class LogoutUserSerializer(serializers.Serializer):

    refresh_token=serializers.CharField()
    
    default_error_message = {
        'bad_token': ('Token is invalid or expired')
    }

    def validate(self, attrs):
        self.token=attrs.get('refresh_token')
        return attrs

    def save (self, **kwargs):
        try:
            token = RefreshToken(self.token)
            token.blacklist()
        except TokenError:
            return self.fail;("bad_token")

class GoogleOauthSignInSerializer(serializers.Serializer):
    access_token=serializers.CharField(min_length=6)


    def validate_access_token(self, access_token):
        google_user_data=Google.validate(access_token)
        try:
            userid=google_user_data["sub"]
            
        except:
            raise serializers.ValidationError("This token has expired or invalid please try again")
        
        if user_data['aud'] != settings.GOOGLE_CLIENT_ID:
                raise AuthenticationFailed('Could not verify user.')
                
        email=google_user_data['email']
        first_name=google_user_data['given_name']
        last_name=google_user_data['family_name']
        provider='google'

        return register_social_user(provider, email, first_name, last_name)


class GithubOauthSignInSerializer(serializers.Serializer):
    code = serializers.CharField()

    def validate_code(self, code):   
        access_token = Github.exchange_code_for_token(code)

        if access_token:
            user_data=Github.get_github_user(access_token)

            full_name=user_data['name']
            email=user_data['email']
            names=full_name.split(" ")
            firstName=names[1]
            lastName=names[0]
            provider='github'
            return register_social_user(provider, email, firstName, lastName)