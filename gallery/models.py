from django.db import models

# Create your models here.

# Test ORM object
class Repo(models.Model):
    github_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=254)
    description = models.TextField()
    svn_url = models.CharField(max_length=254)
    watchers = models.IntegerField()
    language = models.CharField(max_length=254, blank=True, null=True)

    def __unicode__(self):
        return self.name
