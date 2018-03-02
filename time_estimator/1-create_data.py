import csv
from collections import Counter
from datetime import datetime
from git import Repo
from os import listdir
from os.path import dirname, join, realpath
from random import random, shuffle
from subprocess import check_output
from utils import *
import time

from config import *

directory = dirname(realpath(__file__))
print("directory:", directory)

path_to_keywords_directory = join(directory, "keywords")
keywords = {}
for language in ["CSS", "JavaScript", "Markdown", "Python", "Ruby"]:
    path_to_keywords_for_language = join(path_to_keywords_directory, language + ".txt")
    with open(path_to_keywords_for_language) as f:
        keywords[language] = f.read().strip("\n").split("\n")

print("keywords:", keywords)

def get_counts_from_diff_text(text):
    counter = Counter()
    filename = None
    language = None
    count_additions = 0
    try:
        diff_lines = text.split(b"\n")
    except TypeError:
        return {}
    
    for diff_line in diff_lines:
        try:
            if diff_line.startswith(b"+++ b/"):
                filename = diff_line.replace(b"+++ b/", b"")
                #print("filename:", filename)
                language = get_language_from_filename(filename)
            elif diff_line.startswith(b"+"):
                count_additions += 1
                if language:
                    #print("addition:", diff_line)
                    try:
                        addition = diff_line.replace(b"+",b"").decode()
                    except Exception as e:
                        print("decoding failed")
                        print(e)
                        continue
                
                    for kw in keywords[language]:
                        counter[language + ":" + kw] = addition.count(kw)
        except Exception as e:
            print("diff_line failed,", e)
            raise e
    counter["count_additions"] = count_additions
    return counter
    
   
def create_data():
    
    start = datetime.now()
    
    print("starting build_model")

    with open(data_path, "w") as output_file:
    
        fieldnames = []
        for language, language_keywords in keywords.items():
            for keyword in language_keywords:
                fieldnames.append(language + ":" + keyword)
        fieldnames = list(set(fieldnames))
        fieldnames.append("count_additions")
        fieldnames.append("duration")
        print("fieldnames:", fieldnames)
    
        output_writer = csv.DictWriter(output_file, fieldnames)
        output_writer.writeheader()
        print("wrote header to ", data_path)

    owners = listdir(path_to_repos)
    print("owners:", owners)

    for owner in owners:
        path_to_owner = join(path_to_repos, owner)
        owned_repos = listdir(path_to_owner)
        for name_of_repo in owned_repos:
            print("name_of_repo:", name_of_repo)
            path_to_repo = join(path_to_owner, name_of_repo)

            commit_ids = get_commit_ids(path_to_repo)
            
            # want to go in consecutive order
            commit_ids.reverse()
            #print("commit_ids:", commit_ids)

            previous_date = None
            for index, commit_id in enumerate(commit_ids):
                shown_text = git_show_commit(commit_id, path_to_repo)
                date = get_date_of_commit(commit_id, path_to_repo)
                counter = get_counts_from_diff_text(shown_text)
                
                sum_of_counts = sum(counter.values())

                if sum_of_counts == 0:
                    #print("got nothing from " + commit_id[:5] + " and " + path_to_repo)
                    #print(shown_text)
                    #print("\n\n")
                    pass
                
                #print("counter:", counter)
                if sum_of_counts and previous_date:
                    duration = (date - previous_date).total_seconds()
                    #print("duration:", duration)
                    if duration > 0:
                        row = counter
                        row["duration"] = duration
                        with open(data_path, "a") as output_file:
                            csv.DictWriter(output_file, fieldnames).writerow(row)
                previous_date = date

    method_duration = (datetime.now() - start).total_seconds()
    print("finishing build_model")
    print("took ", method_duration, "seconds")
    
create_data()