from django.conf.urls import patterns, include, url
from django.contrib import admin
from gallery.views import github_hook, allReposAndContributersJSON

urlpatterns = patterns(
  '',
  url(r'^admin/', include(admin.site.urls)),
  url(r'^github-hook/$', github_hook),
  url(r'^json/$', allReposAndContributersJSON),

)
