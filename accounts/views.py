from rest_framework import status 
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny,IsAuthenticated
from django.core.mail import send_mail
from django.conf import settings
from .serializers import RegisterSerializer,ProfileSerializer,ChangePasswordSerializer
from .models import CustomUser , OTPVerification
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from django.contrib.auth import authenticate




#API FOR REGISTER 
class RegisterView(APIView):
    permission_classes  =[AllowAny]

    def post(self,request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            user.is_active = False
            user .save()

            otp_obj ,created = OTPVerification.objects.get_or_create(user=user)
            otp = otp_obj.generate_otp()

            send_mail(
                subject = 'verify your TextChat account',
                message=f'your OTP is: {otp} \n Valid for 10 minutes.',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[user.email],
                fail_silently=False
            )
            return Response({
                'message' : 'Registeration successfull check your email for OTP',
                'email':user.email
            },status=status.HTTP_201_CREATED)
        
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    
# RESENDING THE OTP TO USER IF NOT GOT FOR THE FIRST REQUEST:

class ResendOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')

        try:
            user= CustomUser.objects.get(email=email)
        except CustomUser .DoesNotExist:
            return Response({
                'error': 'No accounts found with this email'},
                 status=status.HTTP_404_NOT_FOUND
            )

        if user .is_active:
            return Response({
                'error' : 'Account already verified:'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        otp_obj, created = OTPVerification.object.get_or_create(user=user)
        otp = otp_obj.generate_otp()

        send_mail(
            subject='TextChat - New OTP',
            message=f'Your new OTP is : {otp} \n Valid for 10 minutes.',
            from_email=settings.Email_HOST_USER,
            recipient_list=[user .email],
            fail_silently=False
        )

        return Response({
            'message': 'New OTP sent to your email!'},
            status=status.HTTP_200_OK

        )

class VerifyOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self,request):
        email = request.data.get('email')
        otp = request.data.get('otp')


        try:

            user = CustomUser.objects.get(email-email)

        except CustomUser.DoesNotExit:
            return Response({
                'error': 'No account found with this email'
            }, status=status.HTTP_404_NOT_FOUND)
        
        try:
            otp_obj = OTPVerification.objects.get(user=user)
        except OTPVerification.DoesNotExit:
            return Response({
                'error': 'No OTP found. Please register again'      
            },status=status.HTTP_404_NOT_FOUND)

        if otp_obj.is_expired():
            return Response({
                'error': 'Invalid OTP . Please try again'
            }, status=status.HTTP_400_BAD_REQUEST)

        user .is_active = True
        otp_obj.save()

        return Response({
            'message': 'Account verfied successfully! You can now login.'
        }, status=status.HTTP_200_OK)    
    
#login view
class LoginView(APIView):
    permission_classes =[AllowAny]

    def post(self,request):
        login_input = request.data.get('login')
        password = request.data.get('password')

        if '@' in login_input:
            try:
                user = CustomUser.objects.get(email=login_input)

            except CustomUser.DoesNotExist:
                return Response({'error': 'invalid credentials'},status=status.HTTP_401_UNAUTHORIZED) 
        elif login_input.isdigit():
            try:
                user = CustomUser.objects.get(phone_number=login_input)
            except CustomUser.DoesNotExist:
                return Response({'error': 'Invalid credentials'} ,status=status.HTTP_401_UNAUTHORIZED)
               
        else:
            try:
                user = CustomUser.objects.get(username=login_input)
            except CustomUser.DoesNotExist:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        if not user.check_password(password):
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        if not user.is_active:
            return Response({'error': 'Account not verified. check your email for OTP'},status=status.HTTP_403_FORBIDDEN) 

        refresh = RefreshToken.for_user(user)

        return Response({
            'message': 'Login Successfull',
            'username': user.username,
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh)

        }, status=status.HTTP_200_OK) 
            
# logout view 
                      
class LogoutView(APIView):
    def post(self,request):
        try:
            refresh_token = request.data.get('refresh_token')
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({
                'message': 'Logged out successfully'
            }, status=status.HTTP_200_OK)
        except TokenError:
            return Response({
                'error': 'Invalid token'
            },status=status.HTTP_400_BAD_REQUEST)
            

    
class ProfileView(APIView):
    def get(self,request):
        serializer = ProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class UpdateProfileView(APIView):
    def put(self,request):
        serializer = ProfileSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'profile updated successfully',
                'data':serializer.data
            }, status=status.HTTP_200_OK)
    
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ChangePasswordView(APIView):
    permission_classes =[IsAuthenticated]

    def post(self,request):
        serializer = ChangePasswordSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({'message':'invalid input'},status=status.HTTP_400_BAD_REQUEST)
        
        user = request.user

        old_password = serializer.validated_data["old_password"]
        new_password = serializer.validated_data['new_password']

        if not user.check_password(old_password):
            return Response({
                "error": "Old password is incorrect"
            },status=status.HTTP_400_BAD_REQUEST)
        
        user.set_password(new_password)
        user.save()

        return Response({
            
            "message": "Password changed successfully"
        },status=status.HTTP_200_ok)

     


