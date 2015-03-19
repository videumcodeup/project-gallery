# -*- coding:utf8 -*-

import json
import httplib
import string

from django.http import HttpResponse
from django.views.generic import ListView, TemplateView
from django.core import serializers

from .models import Repo, Contributor

# Removing unwanted chars to slug
def create_slug(text):
    slug_string = ''
    for i in text:
        if i in string.ascii_letters:
            slug_string += i
    return slug_string

def getThingsFromGithubAPI(url):
    connection = httplib.HTTPSConnection('api.github.com')
    connection.request('GET', url, {}, {'User-Agent':'videumcodeup'})
    data = json.loads(connection.getresponse().read())

    return data

def getContributors(repo):
    data = getThingsFromGithubAPI('/repos/videumcodeup/'+repo+'/stats/contributors')
    return data

def updateContributersOnAllRepos():

    for i in Repo.objects.all():
        contributors = getContributors(i.name)
        for j in contributors:
            print(j['author']['login']+' contributes to '+i.name)

            # In contributor dont exist in database, add her
            if ( int(j['author']['id']) not in [k.github_id for k in Contributor.objects.all()]):
                    new_contributor = Contributor(
                        name = j['author']['login'],
                        github_id = j['author']['id'],
                        slug = j['author']['login'],
                        html_url = j['author']['html_url'],
                        avatar_url = j['author']['avatar_url'],
                    )

                    new_contributor.save()
                    new_contributor.repos.add(i)

            if ( int(j['author']['id']) in [k.github_id for k in Contributor.objects.all()]):
                contributer = Contributor.objects.get(github_id=j['author']['id'])
                contributer.repos.add(i)

# returns a JSON object
def getReposFromGithubAndSaveIfNotInDatabase():
    repos_from_github = getThingsFromGithubAPI('/orgs/videumcodeup/repos')

    for i in repos_from_github:

        # If repo not in database, add it and its contributers
        if i['id'] not in [j.github_id for j in Repo.objects.all()]:
            new_repo = Repo(
                github_id = i['id'],
                slug = create_slug(i['name']),
                name = i['name'],
                description = i['description'],
                html_url = i['svn_url'],
                watchers = i['watchers'],
                language = i['language']
            )
            new_repo.save()

            # Get contributors from repo
            contributers = getContributors(i['name'])

            for k in contributers:
                if k['author']['id'] not in [j.github_id for j in Contributor.objects.all()]:
                    new_contributor = Contributor(
                        name = k['author']['login'],
                        github_id = k['author']['id'],
                        slug = k['author']['login'],
                        html_url = k['author']['html_url'],
                        avatar_url = k['author']['avatar_url'],
                    )

                    new_contributor.save()
                    new_contributor.repos.add(new_repo)

    updateContributersOnAllRepos()

    return True


def github_hook(request):
    if getReposFromGithubAndSaveIfNotInDatabase() == True:
          return HttpResponse(json.dumps({'status':'ok'}), content_type='application/json')
    else:
        return HttpResponse(json.dumps({'status':'fail'}), content_type='application/json')

def allReposAndContributersJSON(request):

    repos_list = []
    contributers_list = []

    for repo in Repo.objects.all():
        repo = {
            'id' : repo.id,
            'name' : repo.name,
            'description' : repo.description,
            'html_url' : repo.html_url,
            'watchers' : repo.watchers,
            'language' : repo.language
        }
        repos_list.append(repo)

    for con in Contributor.objects.all():
        contributer = {
            'name' : con.name,
            'html_url' : con.html_url,
            'avatar_url' : con.avatar_url,
            'repos' : [r.id for r in con.repos.all()]
        }
        contributers_list.append(contributer)

    data = {
        'repos':repos_list,
        'contributers':contributers_list
    }

    return HttpResponse(json.dumps(data), content_type='application/json')

class TestView(ListView):
    model = Repo
    template_name = 'gallery/test_view.html'


class JsonTesterTemplate(TemplateView):
    template_name = 'gallery/test_view_json.html'