from rest_framework import serializers

from storage.api.serializers import FileSerializer
from users.models import CustomUser


class CustomUserSerializer(serializers.HyperlinkedModelSerializer):
    files = FileSerializer()

    class Meta:
        model = CustomUser
        fields = ("id", "email", "files")


class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta:
        model = CustomUser
        fields = ("email", "password", "password2")
        extra_fields = {"password": {"write_only": True}}

    def save(self):
        account = CustomUser(email=self.validated_data["email"])
        password = self.validated_data["password"]
        password2 = self.validated_data["password2"]

        if password != password2:
            raise serializers.ValidationError({"detail": "Password mast match."})

        account.set_password(password)
        account.save()
        return account
