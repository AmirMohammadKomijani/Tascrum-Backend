from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer , UserSerializer as BaseUserSerializer

class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id','first_name','last_name','occupation','username','email','password']


class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = ['email','username','password']