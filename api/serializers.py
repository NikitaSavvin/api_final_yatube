from rest_framework import serializers

from .models import Comment, Post, Group, Follow

from rest_framework.validators import ValidationError, UniqueTogetherValidator

class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta: 
        fields = '__all__' 
        model = Post 


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta: 
        read_only_fields = ('post',) 
        fields = '__all__' 
        model = Comment 


class GroupSerializer(serializers.ModelSerializer):

    class Meta: 
        fields = '__all__' 
        model = Group


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )
    following = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )
    
    def validate(self, data):
        user = self.context['request'].user
        following = data.get('following')
        if user == following:
            raise ValidationError('Подписываться на себя нельзя')
        return data
    
    class Meta:
        fields = ('user', 'following')
        model = Follow
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=['user', 'following']
            )
        ]
