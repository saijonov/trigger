from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from PIL import Image
from io import BytesIO
from django.core.files import File

class BucketListItem(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_items')
    date_created = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)
    views = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('item-detail', kwargs={'pk': self.pk})
    
    class Meta:
        ordering = ['-date_created']

class CompletedItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='completed_items')
    bucket_item = models.ForeignKey(BucketListItem, on_delete=models.CASCADE, related_name='completions')
    description = models.TextField()
    photo = models.ImageField(upload_to='completions/')
    date_completed = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} completed {self.bucket_item.title}"
    
    def get_absolute_url(self):
        return reverse('completion-detail', kwargs={'pk': self.pk})
    
    def compress_image(self):
        """Compress the uploaded image while maintaining aspect ratio"""
        if not self.photo:
            return
            
        # Open the image
        img = Image.open(self.photo)
        
        # Convert to RGB if necessary
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Set maximum dimensions
        max_width = 1200
        max_height = 1200
        
        # Calculate new dimensions while maintaining aspect ratio
        ratio = min(max_width/img.width, max_height/img.height)
        new_size = (int(img.width * ratio), int(img.height * ratio))
        
        # Resize image
        img = img.resize(new_size, Image.Resampling.LANCZOS)
        
        # Save the compressed image
        output = BytesIO()
        img.save(output, format='JPEG', quality=85, optimize=True)
        output.seek(0)
        
        # Update the ImageField
        self.photo = File(output, name=self.photo.name)
    
    def save(self, *args, **kwargs):
        # Compress image before saving if it's a new file
        if not self.pk:  # Only compress on first save
            self.compress_image()
        super().save(*args, **kwargs)
    
    class Meta:
        ordering = ['-date_completed']
        
class ItemView(models.Model):
    item = models.ForeignKey(CompletedItem, on_delete=models.CASCADE, related_name='item_views')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']