from .models import CinemaWallet

class WalletService:
    def init_wallet(self, user):
        new_wallet = CinemaWallet()
        new_wallet.user(user)
        new_wallet.balance = 0
        new_wallet.save()
