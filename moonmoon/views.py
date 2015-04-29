from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse
from github import Github
from github_app_settings import CLIENT_ID, CLIENT_SECRET
import requests as req
from uritemplate import expand
# Create your views here.


def index(request):
    # return HttpResponse("This view if authenticated lists repo or provides login with github option")
    g = build_py_github(request)
    if g is None:
        return render(request, "moonmoon/index.html", {
            "github_authorize_url": "https://github.com/login/oauth/authorize?client_id=" + CLIENT_ID + "&scope=repo,user:email,admin:repo_hook"})
        # return render(request, 'moonmoon/index.html', {"repo_list": repo_list})
    else:
        try:
            return render(request, "moonmoon/index_authenticated.html", {
                "github_authorize_url": "https://github.com/login/oauth/authorize?client_id=" + CLIENT_ID + "&scope=repo,user:email,admin:repo_hook",
                "repos": g.get_user().get_repos(), "user": g.get_user(),
                "github_scopes": request.session["github_scopes"], })

        except GithubException:
            return render(request, "moonmoon/index.html",
                          {"github_authorize_url": "https://github.com/login/oauth/authorize?client_id=" + CLIENT_ID, })


def callback(request):
    code = request.GET["code"]
    url = "https://github.com/login/oauth/access_token"
    headers = {"Accept": "application/json"}
    params = {"client_id": CLIENT_ID, "client_secret": CLIENT_SECRET, "code": code}
    r = req.post(url=url, params=params, headers=headers).json()
    request.session["github_token"] = r["access_token"]
    if r["scope"] == "":
        request.session["github_scopes"] = []
    else:
        request.session["github_scopes"] = r["scope"].split(",")
        return redirect("index")


def payload(request):
    return HttpResponse("This view receives the payload from github.")


def show(request):
    return HttpResponse("This view queries db of user payloads.")


def build_py_github(request):
    token = request.session.get("github_token")
    if token is None:
        return None
    else:
        return Github(login_or_token=token, client_id=CLIENT_ID, client_secret=CLIENT_SECRET)