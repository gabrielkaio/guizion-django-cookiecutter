from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from {{cookiecutter.project_name}}.apps.accounts.models import User
from rest_framework import validators


class UserSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(
        validators=[
            validators.UniqueValidator(
                queryset=User.objects.all(),
                message=_("This e-mail is already registered"),
            )
        ]
    )

    class Meta:
        model = User
        exclude = ('is_superuser', 'is_staff', 'is_active', 'last_login', 'date_joined', 'user_permissions', 'groups',
                   'updated_at', )
        extra_kwargs = {'password': {'write_only': True}, 'id': {'read_only': True}}

    def create(self, validated_data):
        email = validated_data.pop('email')
        password = validated_data.pop('password')

        user = User.objects.create_user(email=email, password=password,
                                        **validated_data)
        return user


class ChangePasswordSerializer(serializers.Serializer):
    last_password = serializers.StringRelatedField()
    new_password = serializers.StringRelatedField()
    confirm_password = serializers.StringRelatedField()
