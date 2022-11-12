from fabric import Config, Connection, task
from invoke import Collection
from invoke.config import merge_dicts

from deploy import git, path


TARGET_FLAG = "--target"
DEFAULT_TARGET = "prod"

production_python = "HKNWEB_MODE=prod python"


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


TARGETS = {
    "prod": {
        "deploy": {
            "name": "prod",
            "branch": "master",
        },
    },
}

CONFIGS = {target: DeployConfig(overrides=config) for target, config in TARGETS.items()}


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


def update(c: Connection):
    print("== Update ==")

    print("-- Creating release")
    git.check(c)
    git.update(c)
    c.commit = git.revision_number(c, c.commit)
    git.create_archive(c)

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


def publish(c: Connection):
    print("== Publish ==")

    print("-- Symlinking current@ to release")
    c.run("ln -sfn {} {}".format(c.release_path, c.current_path), echo=True)

    print("-- Restarting systemd unit")
    c.run("systemctl --user restart hknweb.service", echo=True)


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


@task
def rollback(c, target=DEFAULT_TARGET, release=None):
    with Connection(c.deploy.host, user=c.deploy.user, config=c.config) as c:
        setup(c, release=release)
        update(c)
        publish(c)


# Please add the "target" parameter if you are adding more @task functions
#  to allow custom targets to be used (regardless if your function itself will use it or not)


if __name__ == "__main__":
    TARGET_KEY = "prod"
    ns = Collection(deploy, rollback)
    ns.configure(CONFIGS[TARGET_KEY])
