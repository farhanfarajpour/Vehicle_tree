from celery.bin.logtool import errors
from rest_framework import serializers, status
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

from vehicle_tree_app.middleware.response import APIResponse
from vehicle_tree_app.models.users import Users



class UserUpdateAndUserListSerializer(serializers.Serializer):
    id = serializers.IntegerField(
        allow_null=False,
        required=True,
        error_messages={
            'null': 'id cannot be null.',
            'invalid': 'Invalid id.',
        }
    )

    first_name = serializers.CharField(
        # allow_blank=True,
        max_length=100,
        error_messages={
            'required': 'Please provide your last name.',
            'blank': 'Last name should not be blank.',
            'max_length': 'message length is larger'
        }
    )

    last_name = serializers.CharField(
        # allow_blank=True,
        max_length=100,
        error_messages={
            'required': 'Please provide your last name.',
            'blank': 'Last name should not be blank.',
            'max_length': 'message length is larger'
        }
    )
    mobile = serializers.CharField(
        # allow_blank=True,
        max_length=11,
        error_messages={
            'required': 'Please provide your phone title.',
            'blank': 'Job title should not be blank.',
            'max_length': 'message length is larger'
        }
    )

class TokenSerializer(serializers.Serializer):
    token = serializers.CharField()
    refreshToken = serializers.CharField()

    @classmethod
    def get_tokens(cls, user):
        access_token = AccessToken.for_user(user)
        refresh_token = RefreshToken.for_user(user)
        return {
            'token': str(access_token),
            'refreshToken': str(refresh_token),
        }


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(
        allow_null=False,
        required=True,
        max_length=10,
        error_messages={
            'null': 'Username cannot be null.',
            'invalid': 'Invalid username.'
        }
    )

    password = serializers.CharField(
        allow_null=False,
        required=True,
        max_length=10,
        error_messages={
            'null': 'Password cannot be null.',
            'invalid': 'Invalid password.',
        }
    )


class UserNumberLoginSerializer(serializers.Serializer):
    mobile = serializers.CharField(
        allow_null=False,
        max_length=11,
        required=True,
        error_messages={
            'null': 'work_number cannot be null.',
            'invalid': 'Invalid mobile number.',
        }
    )


class UserNumberCodeSerializer(serializers.Serializer):
    code = serializers.CharField(
        allow_null=False,
        required=True,
        error_messages={
            'null': 'code cannot be null.',
            'invalid': 'Invalid code.',
        }
    )
    mobile = serializers.CharField(
        allow_null=False,
        max_length=11,
        required=True,
        error_messages={
            'null': 'work_number cannot be null.',
            'invalid': 'Invalid mobile number.',
        }
    )


class UserLogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(
        allow_null=False,
        required=True,
        error_messages={
            'null': 'Refresh token cannot be null.',
            'invalid': 'Invalid refresh token.',
        }
    )


class UserDeleteSerializer(serializers.Serializer):
    id = serializers.IntegerField(
        allow_null=False,
        required=True,
        error_messages={
            'null': 'id cannot be null.',
            'invalid': 'Invalid id.',
        }
    )


class CreateUserSerializer(serializers.Serializer):
    username = serializers.CharField(
        allow_null=False,
        required=True,
        max_length=10,
        error_messages={
            'null': 'Username cannot be null.',
            'invalid': 'Invalid username.'
        }
    )
    password = serializers.CharField(
        allow_null=False,
        max_length=10,
        required=True,
        error_messages={
            'null': 'Password cannot be null.',
            'invalid': 'Invalid password.',
        }
    )


class ChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        allow_null=False,
        max_length=10,
        required=True,
        error_messages={
            'null': 'Password cannot be null.',
            'invalid': 'Invalid password.',
        }
    )
    confirm_password = serializers.CharField(
        allow_null=False,
        max_length=10,
        required=True,
        error_messages={
            'null': 'Confirm password cannot be null.',
            'invalid': 'Invalid password.',
        }
    )

    def validate(self, data):
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        if password != confirm_password:
            raise serializers.ValidationError(detail="password_mismatch", code="password_mismatch")
        return data


class RefreshTokenSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(
        allow_null=False,
        required=True,
        error_messages={
            'null': 'Refresh token cannot be null.',
            'invalid': 'Invalid refresh token.',
        }
    )
    def validate(self, data):
        refresh_token = data.get('refresh_token')
        if refresh_token is None:
            raise serializers.ValidationError(detail="refresh_token_null", code="refresh_token_null")
        return refresh_token
