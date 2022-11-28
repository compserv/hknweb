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
    GITHUB_ACTIONS = os.path.join(CONFIG_DIR, "github_actions.json")
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
    print(f"release: {c.release}")
    print(f"commit: {c.commit}")

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
        c.run(f"mkdir -p {d}")


def update(c: Connection):
    print("== Update ==")

    if c.deploy.use_local_repo:
        c.deploy.repo_url = (
            c.run("git config --get remote.origin.url").stdout.strip() + ".git"
        )
        c.commit = c.run("git rev-parse HEAD").stdout.strip()

        c.run(f"git clone --bare {c.deploy.repo_url} {c.repo_path}", echo=True)

    file_exists = lambda p: c.run(f"[[ -f {p} ]]", warn=True).ok
    repo_exists = file_exists(f"{c.repo_path}/HEAD")

    if repo_exists:  # fetch
        with c.cd(c.repo_path):
            c.run(f"git remote set-url origin {c.deploy.repo_url}", echo=True)
            c.run("git remote update", echo=True)
            c.run(f"git fetch origin {c.commit}:{c.commit}", echo=True)
    else:  # clone
        c.run(f"git clone --bare {c.deploy.repo_url} {c.repo_path}", echo=True)

    with c.cd(c.repo_path):
        print("-- Creating git archive for release")
        revision = c.commit
        revision_number = c.run(
            f"git rev-list --max-count=1 {revision} --", echo=True
        ).stdout.strip()
        c.commit = revision_number

        c.run(f"git archive {c.commit} | tar -x -f - -C '{c.release_path}'", echo=True)

    with c.cd(c.release_path):
        print("-- Symlinking shared files")
        c.run(f"ln -s {c.shared_path}/media ./media", echo=True)

        if c.deploy.run_blackbox_postdeploy:
            print("-- Decrypting secrets")
            c.run("blackbox_postdeploy", echo=True)
        else:
            print("-- Skipping decrypting secrets")

    with c.cd(c.release_path):
        print("-- Updating environment")
        c.run(f"bash ./scripts/setup_env.sh {c.deploy.conda_env}", echo=True)


def publish(c: Connection) -> None:
    print("== Publish ==")

    print("-- Symlinking current@ to release")
    c.run(f"ln -sfn {c.release_path} {c.current_path}", echo=True)

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


@task
def deploy_github_actions(c, target=None):
    with Connection(c.deploy.host, user=c.deploy.user, config=c.config) as c:
        c.run = c.local
        setup(c)
        update(c)

        """
        The local publish flow is slightly different than the default deploy publish flow.
        We don't use systemctl to restart a service; instead, we use a custom run script
        """
        print("== Publish ==")

        print("-- Symlinking current@ to release")
        c.run(f"ln -sfn {c.release_path} {c.current_path}", echo=True)

        print("-- Skipping restarting systemd unit")

        with c.cd(c.current_path):
            print("-- Starting server")
            c.run("bash ./scripts/run_github_actions.sh &")


def configure_namespace() -> Collection:
    hknweb_mode = os.environ["HKNWEB_MODE"].lower()
    if hknweb_mode == "dev":
        config_file = ConfigFiles.GITHUB_ACTIONS
        deploy = deploy_github_actions
    elif hknweb_mode == "prod":
        config_file = ConfigFiles.PROD
    else:
        raise ValueError(f"HKNWEB_MODE '{hknweb_mode}' is not a valid value")

    config_dict = json.load(open(config_file))
    config = DeployConfig(overrides=config_dict)

    ns = Collection(deploy=deploy, rollback=rollback)
    ns.configure(config)

    return ns


ns = configure_namespace()
