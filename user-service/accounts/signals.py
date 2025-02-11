from allauth.socialaccount.signals import social_account_added
from django.dispatch import receiver

@receiver(social_account_added)
def social_login_handler(request, sociallogin, **kwargs):
    user = sociallogin.user
    user.provider = sociallogin.account.provider
    if user.provider == 'google':
        user.profile_picture = sociallogin.account.extra_data.get('picture')
    user.save()