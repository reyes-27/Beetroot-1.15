from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Post

@receiver(post_save, sender=Post)
def add_parent_children(sender, instance, created, **kwargs):
    if created:
        print(instance)
        if instance.parent != None:
            parent=instance.parent
            parent=Post.objects.get(id=parent.id)
            parent.repost.add(instance)
        