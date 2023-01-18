from django.db import models

# Create your models here.

class Category(models.Model):
    name=       models.CharField(max_length=255)
    slug=       models.SlugField()
    views=      models.IntegerField(default=0)
    parent=     models.ForeignKey("self", on_delete=models.CASCADE, blank=True, null=True)
    def __str__(self):
        return self.name

    def get_view_count(self):
        views=ViewCount.objects.filter(category=self).count()
        return views

    class Meta:
        verbose_name="Category"
        verbose_name_plural="Categories"

class ViewCount(models.Model):
    category=       models.ForeignKey(Category, related_name="category_view_count", on_delete=models.CASCADE)
    ip_address=     models.CharField(max_length=255)
    def __str__(self):
        return f"{self.ip_address}"