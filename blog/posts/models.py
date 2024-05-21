from django.db import models
from django.contrib.auth import get_user_model
from blog.utils.base_class import BaseModel
User = get_user_model()

# Create your models here.

def post_images_upload_location(instance, filename: str) -> str:
    """Get Location for user profile photo upload."""
    return f"posts/images/{filename}"



class Post(BaseModel):
    CATEGORY_CHOICES = [
    ('travel', 'Travel'),
    ('food_cooking', 'Food and Cooking'),
    ('health_wellness', 'Health and Wellness'),
    ('lifestyle', 'Lifestyle'),
    ('education', 'Education'),
    ]
    
    POST_CHOICES = [
                    ("draft", "draft"), 
                    ("published", "published")
        ]
    title = models.CharField(max_length=200, blank=False, null=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    post_state = models.CharField(max_length=15, default=POST_CHOICES[0][0], choices=POST_CHOICES)
    category = models.CharField(max_length=20, choices= CATEGORY_CHOICES, null=False, blank=False)

    
    def __str__(self) -> str:
        return self.title[:30]

class PostImage(BaseModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_images')
    image = models.ImageField(upload_to=post_images_upload_location)

    def __str__(self) -> str:
        return self.image.name


class PostComment(BaseModel):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="post_comment"
    )
    parent_comment = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.CASCADE, related_name="children"
    )
    user_that_comment = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()

    def __str__(self):
        return self.comment[:20]


class CommentToPostImages(BaseModel):

    comment_to_post = models.ForeignKey(
        PostComment, on_delete=models.CASCADE, related_name="comment_to_post_images"
    )
    post_image = models.ImageField(
        upload_to=post_images_upload_location, blank=True, null=True
    )



class PostReaction(BaseModel):
    REACTION_CHOICES = [
        ("upvote", "upvote"),
        ("downvote", "downvote"),
    ]

    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="comment_to_post_reaction"
    )
    user_that_react = models.ForeignKey(User, on_delete=models.CASCADE)
    reaction = models.CharField(
        max_length=20, null=False, blank=False, choices=REACTION_CHOICES
    )

    def __str__(self) -> str:
        return f"{self.reaction}"