from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .services import AuthService, UserService
from rest_framework.views import APIView
from .serializers import UserSignupSerializer, LoginSerializer

@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    authService = AuthService()
    userService = UserService()
    
    serializer = UserSignupSerializer(data=request.data)
    if not serializer.is_valid():
        return Response({
        'message': 'Registration failed',
        'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    data = serializer.validated_data

    validation_result = authService.validate_signup_credentials(data)
    if not validation_result.is_success():
        return Response({
        'message': 'Registration failed',
        'errors': validation_result.get_error_message()
        }, status=status.HTTP_400_BAD_REQUEST)

    user = userService.create(data)
    tokens = authService.procces_signup(user)

    return Response({
        'message': 'Registration successful',
        'tokens': tokens,
        'user': {
            'id': user.id,
            'email': user.email,
            'phone': user.phone
        }
    }, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer
    authService = AuthService()

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():            
            return Response({
                'message': 'Login failed',
                'errors': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)

        login_result = self.authService.validate_login(serializer.validated_data)
        if not login_result.is_success():
             return Response({
                'message': 'Login failed',
                'errors': login_result.get_error_message()
                }, status=status.HTTP_400_BAD_REQUEST)

        user = login_result.get_data()
        tokens = self.authService.procces_login(user)

        return Response({
                'message': 'Registration successful',
                'tokens': tokens,
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'phone': user.phone
                }
            }, status=status.HTTP_201_CREATED)

        
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    authService = AuthService()

    refresh_token = request.data.get('refresh_token')
    if not refresh_token:
        return Response({
            'message': 'Refresh token is required',
        }, status=status.HTTP_400_BAD_REQUEST)

    authService.proccess_logout(refresh_token)
    
    return Response({
        'message': 'Logout successful'
    }, status=status.HTTP_200_OK)
   