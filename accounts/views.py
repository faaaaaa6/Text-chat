from rest_framework import status 
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.core.mail import send_mail
from django.conf import settings
from .serializers import RegisterSerializer
from .models import CustomUser , OTPVerification

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