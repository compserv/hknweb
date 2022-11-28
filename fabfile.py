import os

import posixpath

import json

from fabric import Config, Connection, task

from invoke import Collection
from invoke.config import merge_dicts


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_DIR = os.path.join(ROOT_DIR, "config", "deploy")


class ConfigFiles:
    SHARED = os.path.join(CONFIG_DIR, "shared.json")
    LOCAL = os.path.join(CONFIG_DIR, "local.json")
    PROD = os.path.join(CONFIG_DIR, "prod.json")


class DeployConfig(Config):
    @staticmethod
    def global_defaults():
        hkn_shared = json.load(open(ConfigFiles.SHARED))
        return merge_dicts(Config.global_defaults(), hkn_shared)


def setup(c: Connection, commit=None, release=None):
    print("== Setup ==")

    # Returns the server date-time, encoded as YYYYMMSS_HHMMSS.
    timestamp = c.run("date +%Y%m%d_%H%M%S").stdout.strip()

    # Point the connection to the correct git config
    c.release = release if release else timestamp
    c.commit = commit if commit else c.deploy.branch
    print("release: {}".format(c.release))
    print("commit: {}".format(c.commit))

    # Setup paths
    c.deploy_path = posixpath.join(c.deploy.path.root, c.deploy.name)
    c.repo_path = posixpath.join(c.deploy_path, c.deploy.path.repo)
    c.releases_path = posixpath.join(c.deploy_path, c.deploy.path.releases)
    c.current_path = posixpath.join(c.deploy_path, c.deploy.path.current)
    c.shared_path = posixpath.join(c.deploy_path, c.deploy.path.shared)
    c.release_path = posixpath.join(c.releases_path, c.release)

    # Create dirs
    dirs = (
        c.repo_path,
        c.deploy_path,
        c.releases_path,
        c.shared_path,
        c.release_path,
    )
    for d in dirs:
        c.run("mkdir -p {}".format(d))


def create_release(c: Connection) -> None:
    # Update git repo
    with c.cd(c.deploy_path):
        file_exists = lambda p: c.run(f"[[ -f {p} ]]", warn=True).ok
        repo_exists = file_exists(f"{c.repo_path}/HEAD")
        if repo_exists:  # fetch
            c.run(f"git remote set-url origin {c.deploy.repo_url}", echo=True)
            c.run("git remote update", echo=True)
            c.run(f"git fetch origin {c.commit}:{c.commit}", echo=True)
        else:  # clone
            c.run(f"git clone --bare {c.deploy.repo_url} {c.repo_path}")

    # Create git archive
    with c.cd(c.repo_path):
        revision = c.commit
        revision_number = c.run(
            f"git rev-list --max-count=1 {revision} --", echo=True
        ).stdout.strip()

        c.commit = revision_number
        c.run(f"git archive {c.commit} | tar -x -f - -C '{c.release_path}'", echo=True)


def update(c: Connection):
    print("== Update ==")

    print("-- Creating release")
    create_release(c)

    with c.cd(c.release_path):
        print("-- Symlinking shared files")
        c.run("ln -s {}/media ./media".format(c.shared_path), echo=True)

        print("-- Decrypting secrets")
        c.run("blackbox_postdeploy", echo=True)

        print("-- Updating conda environment")
        c.run("conda update -f config/hknweb-prod.yml", echo=True)

        with c.prefix("conda activate hknweb-prod"):
            print("-- Migrating tables")
            c.run("python manage.py migrate")

            print("-- Collecting static files")
            c.run("python manage.py collectstatic --noinput")


def publish(c: Connection) -> None:
    print("== Publish ==")

    print("-- Symlinking current@ to release")
    c.run("ln -sfn {} {}".format(c.release_path, c.current_path), echo=True)

    print("-- Restarting systemd unit")
    c.run("systemctl --user restart hknweb.service", echo=True)


"""
For the following @task functions, "target" is an ignored parameter. It is a workaround to
allow for use in using command line arguments for selecting a "target" in ns.configure. 
Otherwise, fabfile will claim to not recognize it.
"""


@task
def deploy(c, target=None, commit=None):
    with Connection(c.deploy.host, user=c.deploy.user, config=c.config) as c:
        setup(c, commit=commit)
        update(c)
        publish(c)


@task
def rollback(c, target=None, release=None):
    with Connection(c.deploy.host, user=c.deploy.user, config=c.config) as c:
        setup(c, release=release)
        update(c)
        publish(c)


def configure_namespace() -> Collection:
    hknweb_mode = os.environ["HKNWEB_MODE"].lower()
    if hknweb_mode == "dev":
        config_file = ConfigFiles.LOCAL
    elif hknweb_mode == "prod":
        config_file = ConfigFiles.PROD
    else:
        raise ValueError("HKNWEB_MODE is not a valid value")

    config_dict = json.load(open(config_file))
    config = DeployConfig(overrides=config_dict)

    ns = Collection(deploy, rollback)
    ns.configure(config)

    return ns


ns = configure_namespace()
