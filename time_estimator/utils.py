from datetime import datetime
from subprocess import check_output
from subprocess import CalledProcessError

def get_date_of_commit(commit_id, repopath):
    cmd = "git show -s --format=%ct " + commit_id
    output = check_output(cmd, cwd=repopath, shell=True)
    timestamp = int(output.strip(b"\n"))
    date_of_commit = datetime.fromtimestamp(timestamp)
    return date_of_commit
    
def get_commit_ids(path_to_repo):
    try:
        cwd = path_to_repo
        log = check_output("git log", cwd=cwd, shell=True)
        log_lines = log.split(b"\n")
        commit_ids = []
        for log_line in log_lines:
            if log_line.startswith(b"commit"):
                commit_id = log_line.replace(b"commit ",b"").decode()
                commit_ids.append(commit_id)
    
        return commit_ids
    except Exception as e:
        return []

def git_show_commit(commit_id, path_to_repo):
    try:
        cmd = "git show " + commit_id
        shown = check_output(cmd, cwd=path_to_repo, shell=True)
        return shown
    except CalledProcessError:
        return ""
    
def get_language_from_filename(filename):
    if filename.endswith(b".rb"):
        return "Ruby"
    elif filename.endswith(b".py"):
        return "Python"
    elif filename.endswith(b".js"):
        return "JavaScript"