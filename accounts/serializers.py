from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.utils.translation import gettext_lazy as _

from .validator import validate_password_match

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'role', 'date_joined')

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    confirm_password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password', 'confirm_password', 'role')
        extra_kwargs = {
            'role': {'required': False}
        }

    def validate(self, attrs):
        return validate_password_match(attrs)

    def create(self, validated_data):
        # Remove confirm_password as it's not part of the User model
        validated_data.pop('confirm_password')
        # Use the custom manager's create_user method
        # The **validated_data syntax unpacks the dictionary into keyword arguments
        user = User.objects.create_user(**validated_data)
        return user

class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login.
    """
    email = serializers.EmailField(label=_("Email"))
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(request=self.context.get('request'), email=email, password=password)
        if not user:
            raise serializers.ValidationError(_('Unable to log in with provided credentials.'), code='authorization')

        attrs['user'] = user
        return attrs

class LogoutSerializer(serializers.Serializer):
    """
    Serializer for logging out a user by blacklisting their refresh token.
    """
    refresh = serializers.CharField()

    default_error_messages = {
        'bad_token': _('Token is invalid or expired')
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')