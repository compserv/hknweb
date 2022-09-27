from fabric import Config
from fabric import Connection
from fabric import task
from invoke import Collection
from invoke.config import merge_dicts

from deploy import git
from deploy import path

import argparse

TARGET_FLAG = "--target"
DEFAULT_TARGET = "prod"


def timestamp(c: Connection) -> str:
    """
    Returns the server date-time, encoded as YYYYMMSS_HHMMSS.
    """
    return c.run("date +%Y%m%d_%H%M%S").stdout.strip()


def create_dirs(c: Connection):
    dirs = (
        c.repo_path,
        c.deploy_path,
        c.releases_path,
        c.shared_path,
        c.release_path,
    )
    for d in dirs:
        c.run("mkdir -p {}".format(d))


class DeployConfig(Config):
    @staticmethod
    def global_defaults():
        hkn_defaults = {
            "deploy": {
                "name": "default",
                "user": "hkn",
                "host": "apphost.ocf.berkeley.edu",
                "path": {
                    "root": "/home/h/hk/hkn/hknweb",
                    "repo": "repo",
                    "releases": "releases",
                    "current": "current",
                    "shared": "shared",
                },
                "repo_url": "https://github.com/compserv/hknweb.git",
                "branch": "master",
                "linked_files": [],
                "linked_dirs": [],
                "keep_releases": 10,
            },
        }
        return merge_dicts(Config.global_defaults(), hkn_defaults)


targets = {
    "prod": {
        "deploy": {
            "name": "prod",
            "branch": "master",
        },
    },
}

configs = {target: DeployConfig(overrides=config) for target, config in targets.items()}

# pprint(vars(configs['prod']))


def create_release(c: Connection):
    print("-- Creating release")
    git.check(c)
    git.update(c)
    c.commit = git.revision_number(c, c.commit)
    git.create_archive(c)


def symlink_shared(c: Connection):
    print("-- Symlinking shared files")
    with c.cd(c.release_path):
        c.run("ln -s {}/media ./media".format(c.shared_path), echo=True)


def decrypt_secrets(c):
    print("-- Decrypting secrets")
    with c.cd(c.release_path):
        c.run("blackbox_postdeploy", echo=True)


def install_deps(c: Connection):
    print("-- Installing dependencies")
    with c.cd(c.release_path):
        c.run("make install-prod")


def django_migrate(c: Connection):
    print("-- Migrating tables")
    with c.cd(c.release_path):
        c.run("HKNWEB_MODE=prod $(CONDA_PREFIX)/python ./manage.py migrate")


def django_collectstatic(c: Connection):
    print("-- Collecting static files")
    with c.cd(c.release_path):
        c.run("HKNWEB_MODE=prod $(CONDA_PREFIX)/python ./manage.py collectstatic --noinput")


def symlink_release(c: Connection):
    print("-- Symlinking current@ to release")
    c.run("ln -sfn {} {}".format(c.release_path, c.current_path), echo=True)


def systemd_restart(c: Connection):
    print("-- Restarting systemd unit")
    c.run("systemctl --user restart hknweb.service", echo=True)


def setup(c: Connection, commit=None, release=None):
    print("== Setup ==")
    if release is None:
        c.release = timestamp(c)
    else:
        c.release = release
    c.deploy_path = path.deploy_path(c)
    c.repo_path = path.repo_path(c)
    c.releases_path = path.releases_path(c)
    c.current_path = path.current_path(c)
    c.shared_path = path.shared_path(c)
    c.release_path = path.release_path(c)
    if commit is None:
        c.commit = c.deploy.branch
    else:
        c.commit = commit
    print("release: {}".format(c.release))
    print("commit: {}".format(c.commit))
    create_dirs(c)
    create_conda(c)


def create_conda(c: Connection):
    c.run("make conda")


def activate_conda(c: Connection):
    c.run("conda activate hknweb")


def update(c: Connection):
    print("== Update ==")
    create_release(c)
    symlink_shared(c)
    decrypt_secrets(c)
    create_conda(c)
    activate_conda(c)
    install_deps(c)
    django_migrate(c)
    django_collectstatic(c)


def publish(c: Connection):
    print("== Publish ==")
    symlink_release(c)
    systemd_restart(c)


def finish(c):
    pass


# For the following @task functions, "target" is an ignored parameter
#  It is a workaround to allow for use in using command line arguments
#  For selecting a "target" in ns.configure
# Otherwise, fabfile will claim to not recognize it


@task
def deploy(c, target=DEFAULT_TARGET, commit=None):
    with Connection(c.deploy.host, user=c.deploy.user, config=c.config) as c:
        setup(c, commit=commit)
        update(c)
        publish(c)
        finish(c)


@task
def rollback(c, target=DEFAULT_TARGET, release=None):
    with Connection(c.deploy.host, user=c.deploy.user, config=c.config) as c:
        setup(c, release=release)
        update(c)
        publish(c)
        finish(c)


# Please add the "target" parameter if you are adding more @task functions
#  to allow custom targets to be used (regardless if your function itself will use it or not)


def get_target(args):
    target = args.target
    if target not in configs:
        message = '\n\tTarget Configuration "{}" is not a valid entry'.format(
            TARGET_FLAG
        )
        message += "\n\tInvalid Entry: " + target
        assert target in configs, message
    return target


parser = argparse.ArgumentParser(
    description='Target parameters for the fab file through the "fab" library'
)
parser.add_argument(
    "--target",
    default="prod",
    help="The Target Configuration key to set the deployment setting",
)
args, unknown = parser.parse_known_args()

target_key = get_target(args)
print("Target Set:", target_key)

ns = Collection(deploy, rollback)
ns.configure(configs[target_key])
