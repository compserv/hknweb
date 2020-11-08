from fabric import Config
from fabric import Connection
from fabric import task
from invoke import Collection
from invoke.config import merge_dicts

from deploy import git
from deploy import path


def timestamp(c: Connection) -> str:
    """
    Returns the server date-time, encoded as YYYYMMSS_HHMMSS.
    """
    return c.run('date +%Y%m%d_%H%M%S').stdout.strip()


def create_dirs(c: Connection):
    dirs = (
        c.repo_path,
        c.deploy_path,
        c.releases_path,
        c.shared_path,
        c.release_path,
    )
    for d in dirs:
        c.run('mkdir -p {}'.format(d))


class DeployConfig(Config):
    @staticmethod
    def global_defaults():
        hkn_defaults = {
            'deploy': {
                'name': 'default',
                'user': 'hkn',
                'host': 'apphost.ocf.berkeley.edu',
                'path': {
                    'root': '/home/h/hk/hkn/hknweb',
                    'repo': 'repo',
                    'releases': 'releases',
                    'current': 'current',
                    'shared': 'shared',
                },
                'repo_url': 'https://github.com/compserv/hknweb.git',
                'branch': 'master',
                'linked_files': [],
                'linked_dirs': [],
                'keep_releases': 10,
            },
        }
        return merge_dicts(Config.global_defaults(), hkn_defaults)


targets = {
    'prod': {
        'deploy': {
            'name': 'prod',
            'branch': 'master',
        },
    },
}

configs = {
    target: DeployConfig(overrides=config)
    for target, config in targets.items()
}

# pprint(vars(configs['prod']))


def create_release(c: Connection):
    print('-- Creating release')
    git.check(c)
    git.update(c)
    c.commit = git.revision_number(c, c.commit)
    git.create_archive(c)


def symlink_shared(c: Connection):
    print('-- Symlinking shared files')
    with c.cd(c.release_path):
        c.run('ln -s {}/venv ./.venv'.format(c.shared_path), echo=True)


def decrypt_secrets(c):
    print('-- Decrypting secrets')
    with c.cd(c.release_path):
        c.run('blackbox_postdeploy', echo=True)


def install_deps(c: Connection):
    print('-- Installing dependencies')
    with c.cd(c.release_path):
        c.run('source .venv/bin/activate && pipenv install --deploy', echo=True, env={'PIPENV_VENV_IN_PROJECT': 'true'})
        c.run('./provision_frontend.sh prod')


def django_migrate(c: Connection):
    print('-- Migrating tables')
    with c.cd(c.release_path):
        c.run('HKNWEB_MODE=prod .venv/bin/python ./manage.py migrate')


def django_collectstatic(c: Connection):
    print('-- Collecting static files')
    with c.cd(c.release_path):
        c.run('HKNWEB_MODE=prod .venv/bin/python ./manage.py collectstatic --noinput')


def symlink_release(c: Connection):
    print('-- Symlinking current@ to release')
    c.run('ln -sfn {} {}'.format(c.release_path, c.current_path), echo=True)


def systemd_restart(c: Connection):
    print('-- Restarting systemd unit')
    c.run('systemctl --user restart hknweb.service', echo=True)


def setup(c: Connection, commit=None, release=None):
    print('== Setup ==')
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
    print('release: {}'.format(c.release))
    print('commit: {}'.format(c.commit))
    create_dirs(c)
    if not path.file_exists(c, '{}/venv/bin/activate'.format(c.shared_path)):
        create_venv(c)


def create_venv(c: Connection):
    c.run('python3.7 -m venv {}/venv'.format(c.shared_path))


def update(c: Connection):
    print('== Update ==')
    create_release(c)
    symlink_shared(c)
    decrypt_secrets(c)
    if not path.dir_exists(c, '{}/venv'.format(c.shared_path)):
        create_venv(c)
    install_deps(c)
    django_migrate(c)
    django_collectstatic(c)


def publish(c: Connection):
    print('== Publish ==')
    symlink_release(c)
    systemd_restart(c)


def finish(c):
    pass


@task
def deploy(c, target=None, commit=None):
    with Connection(c.deploy.host, user=c.deploy.user, config=c.config) as c:
        setup(c, commit=commit)
        update(c)
        publish(c)
        finish(c)


@task
def rollback(c, release=None):
    with Connection(c.deploy.host, user=c.deploy.user, config=c.config) as c:
        setup(c, release=release)
        update(c)
        publish(c)
        finish(c)


ns = Collection(deploy, rollback)
ns.configure(configs['prod'])
