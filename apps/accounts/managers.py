from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        email=self.normalize_email(email)
        user=self.model(email=email, username=username)
        user.set_password(password)
        user.is_active=True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user=self.create_user(email=email, username=username, password=password)
        user.is_superuser=True
        user.is_staff=True
        user.save(using=self._db)
        return user