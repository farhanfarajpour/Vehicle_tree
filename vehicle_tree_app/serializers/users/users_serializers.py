from rest_framework import serializers
from vehicle_tree_app.models.users import Users


class UserUpdateSerializer(serializers.Serializer):
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


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(
        allow_null=False,
        required=True,
        error_messages={
            'null': 'Username cannot be null.',
            'invalid': 'Invalid username.'
        }
    )

    password = serializers.CharField(
        allow_null=False,
        required=True,
        error_messages={
            'null': 'Password cannot be null.',
            'invalid': 'Invalid password.',
        }
    )


class UserNumberLoginSerializer(serializers.Serializer):
    mobile = serializers.CharField(
        allow_null=False,
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
        required=True,
        error_messages={
            'null': 'work_number cannot be null.',
            'invalid': 'Invalid mobile number.',
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
        error_messages={
            'null': 'Username cannot be null.',
            'invalid': 'Invalid username.'
        }
    )
    password = serializers.CharField(
        allow_null=False,
        required=True,
        error_messages={
            'null': 'Password cannot be null.',
            'invalid': 'Invalid password.',
        }
    )

class ChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        allow_null=False,
        required=True,
        error_messages={
            'null': 'Password cannot be null.',
            'invalid': 'Invalid password.',
        }
    )
    confirm_password = serializers.CharField(
        allow_null=False,
        required=True,
        error_messages={
            'null': 'Confirm password cannot be null.',
            'invalid': 'Invalid password.',
        }
    )