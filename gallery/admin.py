from django.contrib import admin

from .models import Repo, Contributor


admin.site.register(Repo)
admin.site.register(Contributor)
