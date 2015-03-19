from django.db import models

# Create your models here.

class Repo(models.Model):
    github_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=254)
    slug = models.SlugField()
    description = models.TextField()
    html_url = models.CharField(max_length=254)
    watchers = models.IntegerField()
    language = models.CharField(max_length=254, blank=True, null=True)

    def __unicode__(self):
        return self.name

class Contributor(models.Model):
    name = models.CharField(max_length=254)
    github_id = models.IntegerField(unique=True)
    html_url = models.CharField(max_length=254)
    slug = models.SlugField()
    avatar_url = models.CharField(max_length=254)
    repos = models.ManyToManyField(Repo, blank=True, null=True)

    def __unicode__(self):
        return self.name