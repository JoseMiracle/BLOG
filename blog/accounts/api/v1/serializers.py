from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from django.db.models import Q

User = get_user_model()


class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "password",
        ]

    def validate(self, attrs):
        return super().validate(attrs)
    

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(validated_data["password"])
        user.save()

        return validated_data
    

class SignInSerializer(serializers.Serializer):
    """
    Serializer for signing in
    """
    
    email_or_username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs: dict):
        """
        This is for validating credentiials for signing in
        """
        
        
        user = User.objects.filter(Q(email=attrs["email_or_username"]) | Q(username=attrs["email_or_username"])).first()
        if user:
            if user.check_password(attrs["password"]):
                return user
            else: 
                raise serializers.ValidationError({
                    "message": "Invalid Password"
                })
               

        else: # This raises error if the user doesn't exist
            raise serializers.ValidationError({
                "message" : "User doesn't exist"
            })
        

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
                "refresh_token": str(refresh),
                "access_token": str(refresh.access_token),
                "profile": UserSerializer(instance).data
                 }


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for changing password
    """

    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(min_length=8, write_only=True)
    confirm_password = serializers.CharField(min_length=8, write_only=True)

    def validate(self, attrs):
        """
        This is for validating the values the user provides in order to change their password
        """
        user = self.context["request"].user
     

        if attrs["new_password"] != attrs["confirm_password"]:
            raise serializers.ValidationError({
                "message": "New password not same as confirm password"
            })

        if user.check_password(attrs["new_password"]):
            raise serializers.ValidationError({
                "messsage": "New pasword can't be same old password"
                }
                )

        if user.check_password(attrs["old_password"]) is False:
            raise serializers.ValidationError({
                "message" : "Invalid old password"
            })

        elif (attrs["old_password"] != attrs["new_password"]) and (
            attrs["new_password"] == attrs["confirm_password"]
        ):
            return attrs

    def update(self, instance, validated_data):
        """
        This is for updating user's password
        """        
        user = self.context["request"].user
        user.set_password(validated_data["confirm_password"])
        user.save()

        return validated_data
    
class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=False)
    
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'image',
        ]

