from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from base_app.models import BaseUser, BaseModel
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

class Candidate(BaseUser):
    web_address=models.URLField(null=True,blank=True)
    cover_letter=models.TextField(null=True,blank=True)
    attachment =models.FileField(upload_to ='uploads/')
    do_you_like_working=models.BooleanField(default=True)
    rating=models.FloatField(default=0.0,null=True,blank=True)
    ip = models.GenericIPAddressField()


class Reviewer(BaseUser):
    pass


class CommentsModel(BaseModel):
    From_coment = models.ForeignKey(Candidate, related_name="related_comment", on_delete=models.CASCADE)
    to_coment = models.ForeignKey(Reviewer, on_delete=models.PROTECT)
    comment = models.TextField()
    star=models.PositiveIntegerField(validators = [
        MaxValueValidator(5),
        MinValueValidator(0),
    ])

@receiver(post_save, sender=CommentsModel)
def findAvRatings(sender, instance, *args, **kwargs):
    try:
        candidate = instance.candidate
        candidate.ratings = float(CommentsModel.objects.filter(candidate=candidate).aggregate(Avg("stars")).get("stars__avg"))
        candidate.save()
    except Exception as e:
            print(e)