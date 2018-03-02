from os.path import isdir
from os.path import isfile
from os.path import join
from os import mkdir
from requests import get
from subprocess import call
from time import sleep

from config import *

print("starting create_data")

def pause(duration):
    print("pausing for " + str(duration) + " seconds")
    sleep(duration)

def get_all_repos():
    base = "https://api.github.com/repositories"
    
    if isfile("/tmp/since.txt"):
        with open("/tmp/since.txt") as f:
            since = f.read().strip()
            print("loaded since " + since)
    else:
        since = 0
        
    for n in range(10):
        print("n:", n)
        url = base + "?since=" + str(since)
        print("getting url: " + url)
        repos = get(url).json()
        print("got it.")
        for repo in repos:
            if type(repo) == str:
                print("UH OH repo is " + repo)
                print("repos:", repos)
            print("yielding repo")
            yield repo
            print("yielded")
        since = str(repo["id"])
        print("since: " + since)
        with open("/tmp/since.txt", "w") as f:
            f.write(since)
        pause(2)
        

def download_repos():

    if not isdir(path_to_repos):
        mkdir(path_to_repos)
        print("created " + path_to_repos)

    for repo in get_all_repos():
        if repo["fork"] is False and repo["private"] is False:
            print("repo passed test")
            owner = repo["owner"]["login"]
            name = repo["name"]
            
            owner_path = join(path_to_repos, owner)
            if not isdir(owner_path):
                mkdir(owner_path)
            
            html_url = repo["html_url"]
            repo_path = join(owner_path, name)
            if not isdir(repo_path):
                pause(2)
                print("cloning " + html_url)
                call(["git","clone", html_url], cwd=owner_path)
            pause(2)
            
    print("finishing create_data")

download_repos()
