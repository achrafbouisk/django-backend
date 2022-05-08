from rest_framework import serializers
from api.models import Post,  User, Comment, Reply

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('__all__') # === fields = ('title','slug', 'category', 'description', 'image', 'date_added', 'last_modified', )

class CommentSerializer(serializers.ModelSerializer):
    
    # post = serializers.Field(source='')
    class Meta:
        model = Comment
        fields = ('__all__')
    
class ReplySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Reply
        fields = ('__all__')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        #what you most enter
        fields = ['id', 'name', 'email', 'password']
        #don't return the pwd
        extra_kwargs = {  
            'password': {'write_only': True}
        }

    #hashing password
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

