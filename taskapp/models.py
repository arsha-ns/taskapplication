from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Task(models.Model):
    title=models.CharField(max_length=100)
    created_date=models.DateTimeField(auto_now_add=True)

    
    status=models.BooleanField(default=False)
    user_object=models.ForeignKey(User,on_delete=models.CASCADE)
    

    def __str__(self):
        return self.title 