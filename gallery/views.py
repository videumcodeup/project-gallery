from django.shortcuts import render
from django.http import HttpResponse
import json
import httplib

# Create your views here.

def github_hook(request):
  conn = httplib.HTTPSConnection('api.github.com')
  conn.request('GET', '/orgs/videumcodeup/repos', {}, {"User-Agent": "videumcodeup"})
  repos = json.loads(conn.getresponse().read())
  # for i in repos:
  #   print(i['']

  data = {"status": "ok"}
  return HttpResponse(json.dumps(repos), content_type='application/json')
