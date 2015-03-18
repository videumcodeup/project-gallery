import json
import httplib

from django.http import HttpResponse
from django.views.generic import ListView

from .models import Repo
# Create your views here.

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
              name = i['name'],
              description = i['description'],
              svn_url = i['svn_url'],
              watchers = i['watchers'],
              language = i['language']
          )
          new_repo.save()

  data = {"status": "ok"}
  return HttpResponse(json.dumps(repos_from_github), content_type='application/json')


class TestView(ListView):
    model = Repo
    template_name = 'gallery/test_view.html'