from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()

class Event(models.Model):
    title = models.CharField(max_length=100)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    location = models.CharField(max_length=255, blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_events')
    participants = models.ManyToManyField(User, related_name='participating_events', blank=True)
    is_public = models.BooleanField(default=True)
    is_completed = models.BooleanField(default=False)



class TodoItem(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='todo_items', null=True, blank=True)
    order = models.IntegerField(default=0)  # 新增字段来存储排序顺序
    completed = models.BooleanField(default=False)  # 添加完成状态字段

    class Meta:
        ordering = ['order']

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.event:
            # 检查是否所有TodoItem都已完成
            all_completed = self.event.todo_items.all().values_list('completed', flat=True)
            self.event.is_completed = all(all_completed)
            self.event.save()


from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Event)
def sync_event_completion_status(sender, instance, **kwargs):
    TodoItem.objects.filter(event=instance).update(completed=instance.is_completed)

