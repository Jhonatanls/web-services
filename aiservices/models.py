import uuid
from django.db import models
from django.utils.text import slugify
from django.db.models.signals import pre_save


class IAService(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(null=False, blank=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


def set_slug(sender, instance, *args, **kwargs):
    if instance.title and not instance.slug:
        slug = slugify(instance.title)

        while IAService.objects.filter(slug=slug).exists():
            slug = slugify(
                '{}-{}'.format(instance.title, str(uuid.uuid4())[:8])
            )
        instance.slug = slug


pre_save.connect(set_slug, sender=IAService)

