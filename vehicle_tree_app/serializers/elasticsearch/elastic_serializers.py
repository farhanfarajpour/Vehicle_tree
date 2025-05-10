from rest_framework import serializers
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken


class LoginItemOfLogsSerializer(serializers.Serializer):
    city = serializers.CharField(
        allow_null=True,
        required=False,
        allow_blank=True,
        error_messages={
            'null': 'city cannot be null.',
            'invalid': 'Invalid city.'
        }
    )

    first_name = serializers.CharField(
        max_length=100,
        allow_blank=True,
        error_messages={
            'null': 'name cannot be null.',
            'blank': 'Name cannot be blank',

        }
    )
    last_name = serializers.CharField(
        max_length=100,
        allow_blank=True,
        error_messages={
            'null': 'last_name cannot be null.',
            'blank': 'last_name cannot be blank'

        }
    )

    username = serializers.CharField(
        max_length=254,
        allow_blank=True,
        error_messages={
            'required': 'Please provide username.',
            'blank': 'username should not be blank.',
            'max_length': 'username length is larger'
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


class SearchWithCitySerializer(serializers.Serializer):
    city = serializers.CharField(
        allow_null=True,
        required=False,
        allow_blank=True,
        error_messages={
            'null': 'city cannot be null.',
            'invalid': 'Invalid city.'
        }
    )


class SearchWithUsernameSerializer(serializers.Serializer):

    username = serializers.CharField(
        max_length=254,
        allow_blank=True,
        error_messages={
            'required': 'Please provide username.',
            'blank': 'username should not be blank.',
            'max_length': 'username length is larger'
        }
    )



class SearchWithLastnameSerializer(serializers.Serializer):
    last_name = serializers.CharField(
        max_length=100,
        allow_blank=True,
        error_messages={
            'null': 'last_name cannot be null.',
            'blank': 'last_name cannot be blank'

        }
    )

class SearchWithFirstnameSerializer(serializers.Serializer):
        first_name = serializers.CharField(
            max_length=100,
            allow_blank=True,
            error_messages={
                'null': 'first_name cannot be null.',
                'blank': 'first_name cannot be blank'

            }
        )