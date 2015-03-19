# -*- coding:utf8 -*-

import json
import httplib
import string

from django.http import HttpResponse
from django.views.generic import ListView, TemplateView
from django.core import serializers

from .models import Repo

# Removing unwanted chars to slug
def create_slug(text):

    slug_string = ''

    for i in text:

        if i in string.ascii_letters:

            slug_string += i

    return slug_string


def github_hook(request):

  conn = httplib.HTTPSConnection('api.github.com')
  conn.request('GET', '/orgs/videumcodeup/repos', {}, {"User-Agent": "videumcodeup"})
  repos_from_github = json.loads(conn.getresponse().read())

  repos_in_database = Repo.objects.all()

  repos_in_database_id = []
  for i in repos_in_database:
      repos_in_database_id.append(i.github_id)

  for i in repos_from_github:

      if i['id'] not in repos_in_database_id:
          new_repo = Repo(
              github_id = i['id'],
              slug = create_slug(i['name']), # passed in create_slug()
              name = i['name'],
              description = i['description'],
              html_url = i['svn_url'],
              watchers = i['watchers'],
              language = i['language']
          )
          new_repo.save()

  data = {"status": "ok"}
  return HttpResponse(json.dumps(repos_from_github), content_type='application/json')


class TestView(ListView):
    model = Repo
    template_name = 'gallery/test_view.html'

def testViewJson(request):

    repos = Repo.objects.all()

    repo_list = []

    repo_object = {'name': '','description':'','html':'','language':''}

    for repo in repos:
        repo_object = {
            'name': repo.name,
            'description':repo.description,
            'html':repo.html_url,
            'language':repo.language
        }

        repo_list.append(repo_object)

    data = {'repos':repo_list}

    return HttpResponse(json.dumps(data), content_type='application/json')

class JsonTesterTemplate(TemplateView):
    template_name = 'gallery/test_view_json.html'