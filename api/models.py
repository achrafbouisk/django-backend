from django.db import models
# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.name

class Category(models.Model):
    category = models.CharField(max_length=100)

    def __str__(self):
        return self.category

class Post(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    # category = models.CharField(max_length=255)
    category =  models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField()
    image = models.FileField(upload_to="images", blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    is_draft = models.BooleanField(default = True)
    class Meta:
        ordering = ['-date_added']

    def __str__(self):
        return self.title


class Comment(models.Model):
    body = models.TextField(blank=False)
    date_added = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Meta:
        ordering = ['date_added']

    def __str__(self):
        return self.body

class Reply(models.Model):
    body = models.TextField(blank=False)
    date_added = models.DateTimeField(auto_now_add=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


    class Meta:
        ordering = ['date_added']

    def __str__(self):
        return self.body

