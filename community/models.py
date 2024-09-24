from django.db import models
from authentication.models import CustomUser
# Create your models here.

class Post(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    blog_title = models.CharField(max_length=255)
    blog_comment = models.TextField()
    img = models.ImageField(upload_to='community-images')
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.PositiveBigIntegerField(default=0)
    
    def __str__(self):
        return self.blog_title
    
class Like(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    

    