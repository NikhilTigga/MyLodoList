from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class UserRegister(AbstractUser):
    email = models.EmailField(unique=True)
    image = models.ImageField(upload_to='userimage/', null=True, blank=True)

    USERNAME_FIELD = 'email'        
    REQUIRED_FIELDS = ['username']  

    def __str__(self):
        return self.email
    

class Task(models.Model):
    user = models.ForeignKey(UserRegister, on_delete=models.CASCADE, related_name="tasks")
    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=200, default='pending')
    score = models.IntegerField(default=100)
    created_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.title