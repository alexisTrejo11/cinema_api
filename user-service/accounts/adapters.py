from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .models import UserRole
from django.http import JsonResponse
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class CustomAccountAdapter(DefaultAccountAdapter):
    def is_ajax(self, request):
        return any([
            request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest',
            request.content_type == 'application/json',
            request.META.get('HTTP_ACCEPT') == 'application/json'
        ])

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def is_ajax(self, request):
        return any([
            request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest',
            request.content_type == 'application/json',
            request.META.get('HTTP_ACCEPT') == 'application/json'
        ])

    def pre_social_login(self, request, sociallogin):
        """
        Invoked just after a user successfully authenticates via a social provider,
        but before the login is actually processed.
        """
        user = sociallogin.user
        provider = sociallogin.account.provider
        extra_data = sociallogin.account.extra_data
        
        # Set user attributes
        user.provider = provider
        user.first_name = extra_data.get('given_name', '')
        user.last_name = extra_data.get('family_name', '')
        user.profile_picture = extra_data.get('picture')
        user.role = UserRole.COMMON_USER

        # Connect to existing user if email exists
        try:
            existing_user = User.objects.get(email=user.email)
            existing_user.social_login(provider, sociallogin.account)
            sociallogin.connect(request, existing_user)
        except User.DoesNotExist:
            pass

def login_redirect(request):
    if request.user.is_authenticated:
        refresh = RefreshToken.for_user(request.user)
        return JsonResponse({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': {
                'id': request.user.id,
                'email': request.user.email,
                'role': request.user.role,
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'profile_picture': request.user.profile_picture,
            }
        })
    else:
        return JsonResponse({'error': 'Usuario no autenticado'}, status=401)