from django.db import models

# Create your models here.


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)  # 自动设置为对象被创建时的时间
    # updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        date_str = self.created_at.strftime('%Y-%m-%d %H:%M')
        return f"Message from {self.name} at {date_str}"
