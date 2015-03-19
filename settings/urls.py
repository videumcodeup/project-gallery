from django.conf.urls import patterns, include, url
from django.contrib import admin
from gallery.views import github_hook, TestView, testViewJson, JsonTesterTemplate

urlpatterns = patterns(
  '',
  url(r'^admin/', include(admin.site.urls)),
  url(r'^github-hook/$', github_hook),
  url(r'^test-view/$', TestView.as_view()),
  url(r'^json/$', testViewJson),
  url(r'^json_template/$', JsonTesterTemplate.as_view()),

)
