from accounts.serializers import ( 
    UserRegistrationSerializer, LoginSerializer, LogoutUserSerializer, 
    PasswordResetRequestSerializer, SetNewPasswordSerializer, GoogleOauthSignInSerializer, 
    GithubOauthSignInSerializer, )
from accounts.utils import ( send_OTP_to_user, )
from accounts.models import ( User, OneTimePassword, )
from django.utils.http import ( urlsafe_base64_decode, )
from django.utils.encoding import ( smart_str, DjangoUnicodeDecodeError, )
from django.contrib.auth.tokens import ( PasswordResetTokenGenerator, )
from django.shortcuts import ( render, )
from rest_framework.generics import ( GenericAPIView, )
from rest_framework.response import ( Response, )
from rest_framework.permissions import ( AllowAny, IsAuthenticated , )   
from rest_framework.decorators import ( api_view, permission_classes, )
from rest_framework import ( status, )
from rest_framework.views import ( APIView, )

# User registration view
class RegisterUserView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserRegistrationSerializer

    def post(self, request):
        user_data = request.data
        serializer = self.get_serializer(data=user_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()  # Create user
            user = serializer.data
            send_OTP_to_user(user_data['email'])  # Send OTP for email verification
            return Response({
                'data': user,
                "message": f"Hello, {user['first_name']}, a passcode has been sent to your email address. Please check your email to verify your account.",
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# User email verification view
class VerifyUserEmailView(GenericAPIView):
    permission_classes = [AllowAny]

    def post(self, request):
        otp_code = request.data.get('otp')
        try:
            user_code_obj = OneTimePassword.objects.get(code=otp_code)  # Find OTP object
            user = user_code_obj.user
            if not user.is_verified:
                user.is_verified = True
                user.save()  # Mark user as verified
                return Response({
                    "message": f"Hello, {user.first_name}, your account has been verified successfully. You can now login to your account."
                }, status=status.HTTP_200_OK)
            return Response({
                "message": f"Code is Invalid. Your account is already verified."
            }, status=status.HTTP_204_NO_CONTENT)
        except OneTimePassword.DoesNotExist:
            return Response({
                "message": "Please enter the correct passcode."
            }, status=status.HTTP_404_NOT_FOUND)

# User login view
class LoginUserView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# View to test authentication
class TestAuthenticationView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            "message": "Authenticated"
        }, status=status.HTTP_200_OK)

# Password reset request view
class PasswordResetRequestView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = PasswordResetRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        return Response({'message': "A password reset link has been successfully sent to your email."}, status=status.HTTP_200_OK)

# Password reset confirmation view
class PasswordResetConfirmView(GenericAPIView):
    permission_classes = [AllowAny]

    def get(self, request, uidb64, token):
        try:
            user_id = smart_str(urlsafe_base64_decode(uidb64))  # Decode user ID from base64
            user = User.objects.get(id=user_id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'message': "Token is invalid or has expired"}, status=status.HTTP_401_UNAUTHORIZED)
            return Response({'success': True, "message": "Credentials Valid", "uidb64": uidb64, "token": token}, status=status.HTTP_200_OK)
        except DjangoUnicodeDecodeError:
            return Response({'message': "Token is invalid or has expired"}, status=status.HTTP_401_UNAUTHORIZED)

# Set new password view
class SetNewPasswordView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'message': "Password reset successful"}, status=status.HTTP_200_OK)

# User logout view
class LogoutUserView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LogoutUserSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()  # Log out the user
        return Response(status=status.HTTP_204_NO_CONTENT)

# Google OAuth sign-in view
class GoogleOauthSignInView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = GoogleOauthSignInSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = ((serializer.validated_data)['access_token'])
        return Response(data, status=status.HTTP_200_OK)

# GitHub OAuth sign-in view
class GithubOauthSignInView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = GithubOauthSignInSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = ((serializer.validated_data)['code'])
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)