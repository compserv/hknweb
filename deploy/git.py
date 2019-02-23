from fabric import Connection

from .path import repo_path, file_exists

def check(c: Connection):
    return remote_reachable(c)

def update(c: Connection):
    if repo_exists(c):
        fetch(c)
    else:
        clone(c)

def repo_exists(c: Connection) -> bool:
    return file_exists(c, "{}/HEAD".format(c.repo_path))

def remote_reachable(c: Connection) -> bool:
    with c.cd(c.repo_path):
        return c.run("git ls-remote {} HEAD".format(c.deploy.repo_url), warn=True).ok

def clone(c: Connection):
    with c.cd(c.deploy_path):
        c.run("git clone --bare {} {}".format(c.deploy.repo_url, c.repo_path))

def fetch(c: Connection):
    with c.cd(c.repo_path):
        c.run("git remote set-url origin {}".format(c.deploy.repo_url), echo=True)
        c.run("git remote update", echo=True)
        c.run("git fetch origin {0}:{0}".format(c.commit), echo=True)

def revision_number(c: Connection, revision: str) -> str:
    with c.cd(c.repo_path):
        return c.run("git rev-parse {}".format(revision)).stdout.strip()

def create_archive(c: Connection):
    with c.cd(c.repo_path):
        c.run("git archive {} | tar -x -f - -C {}".format(c.commit, c.release))
