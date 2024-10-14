from django.contrib.auth.models import ( BaseUserManager, )
from django.core.exceptions import ( ValidationError, )
from django.core.validators import ( validate_email, )
from django.utils.translation import ( gettext_lazy as _, )

# Custom manager for User model to handle user creation logic
class UserManager(BaseUserManager):

    # Validates if the provided email is in a valid format
    def email_validator(self, email): 
        try:
            validate_email(email)  # Uses Django's built-in email validator
        except ValidationError as e:
            raise ValueError(_("Please provide a valid email address"))

    # Method to create a regular user (non-superuser)
    def create_user(self, email, first_name, last_name, password, **extra_fields):
        if email: 
            email = self.normalize_email(email)  # Normalize the email (e.g., lowercasing domain part)
            self.email_validator(email)  # Validate the email format
        else:
            raise ValueError(_("Email is required"))  # Email is mandatory
        
        # Ensure first_name, last_name, and password are provided
        if not first_name:
            raise ValidationError(_("First name is required"))
        if not last_name:
            raise ValidationError(_("Last name is required"))
        if not password:
            raise ValidationError(_("Password is required"))

        # Create user model instance with provided fields
        user = self.model(
            email=self.normalize_email(email), 
            first_name=first_name, 
            last_name=last_name, 
            **extra_fields
        )
        
        user.set_password(password)  # Set password for the user
        user.save(using=self._db)  # Save user object in the database
        return user

    # Method to create a superuser (admin user)
    def create_superuser(self, email, first_name, last_name, password, **extra_fields):
        # Ensure superuser has the appropriate permissions
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_verified', True)

        # Raise errors if any of the superuser fields are not correctly set
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_("Superuser must have is_staff=True"))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_("Superuser must have is_superuser=True"))
        if extra_fields.get('is_verified') is not True:
            raise ValueError(_("Superuser must have is_verified=True"))

        # Use the create_user method to create a superuser
        user = self.create_user(email, first_name, last_name, password, **extra_fields)
        user.save(using=self._db)  # Save superuser in the database
        return user
