# accounts/models.py
from django.db import models
from django.contrib.auth.models import User

# In models.py - change the field name
class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200,blank=True,null=True)
    text = models.TextField(blank=True)  # Changed from 'content' to 'text'
    drawing = models.ImageField(upload_to='note_drawings/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title