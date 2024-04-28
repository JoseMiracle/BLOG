from rest_framework import serializers
from blog.posts.models import (
    Post, 
    PostImage, 
    PostComment, 
    CommentToPostImages,
    PostReaction
    
)

from django.utils import timezone
from blog.accounts.api.v1.serializers import (
    UserSerializer
)

class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = ["id", "image"]


class PostSerializer(serializers.ModelSerializer):
    
    images = PostImageSerializer(many=True, read_only=True)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(required=False),
        required=False,
    )
    content = serializers.CharField(required=False)

    class Meta:
        model = Post
        fields = [
            "id", 
            "title",
            "content", 
            "category",
            "post_state",
            "content",
            "images", 
            "uploaded_images",
            ]
    

    def create(self, validated_data):

        post_obj = Post.objects.create(
            author=self.context["request"].user,
            content=validated_data["content"],
            title=validated_data['title'],
            post_state=validated_data["post_state"],
            category=validated_data['category']
        )

        post_images = validated_data.pop("uploaded_images", None)

        if post_images is not None:
            for post_image in post_images:
                PostImage.objects.create(post=post_obj, image=post_image)

        return post_obj

    



class UpdatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["post_details", "post_state"]

    def update(self, instance, validated_data):
        if "post_state" in validated_data:
            instance.created_at, instance.last_modified_at = (
                timezone.now(),
                timezone.now(),
            )
            instance.save()
        return super().update(instance, validated_data)
    

class CommentToPostImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentToPostImages
        fields = [
            # "comment_to_post",
            "post_image"
        ]


class PostCommentSerializer(serializers.ModelSerializer):
    comment_to_post_images = CommentToPostImagesSerializer(read_only=True, many=True)
    user_that_comment = UserSerializer(read_only=True)
    uploaded_comment_to_post_images = serializers.ListField(
        child=serializers.ImageField(allow_empty_file=False), max_length=2,
        write_only=True, required=False
    )

    class Meta:
        model = PostComment
        fields = [
            "id",
            "user_that_comment",
            "comment",
            "comment_to_post_images",
            "uploaded_comment_to_post_images",
        ]

  
    def create(self, validated_data):
        uploaded_comment_to_post_images = validated_data.pop(
            "uploaded_comment_to_post_images", None
        )


        comment_to_post_obj = PostComment.objects.create(
            post_id=self.context['post_id'],
            comment=validated_data["comment"],
            user_that_comment=self.context["request"].user,
        )

        if uploaded_comment_to_post_images is not None:
            for comment_to_post_image in uploaded_comment_to_post_images:
                CommentToPostImages.objects.create(
                    comment_to_post=comment_to_post_obj,
                    post_image=comment_to_post_image,
                )
        return comment_to_post_obj


class PostReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostReaction
        fields = [
            'reaction',
            'post',
        ]

    def validate(self, attrs):
        return super().validate(attrs)

    def create(self, validated_data):
        post_reaction_obj, created = PostReaction.objects.get_or_create(
            post=validated_data["post"],
            user_that_react=self.context["request"].user,
            defaults={
                "user_that_react": self.context["request"].user,
                "reaction": validated_data["reaction"],
            },
        )

        if not created:
            post_reaction_obj.reaction = validated_data["reaction"]
            post_reaction_obj.save()
            return post_reaction_obj

        return super().create(validated_data)