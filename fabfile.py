from fabric.api import *
from conf.fabric import config


@task()
def environment(env_name):
    environment = config.ENVIRONMENTS[env_name]
    env.user = environment['user']
    env.hosts = environment['hosts']
    env.path = environment['path']
    env.use_settings = environment['settings']
    env.name = env_name


@task
def prepare_environment():
    sudo("apt-get install aptitude")
    sudo("aptitude update && aptitude upgrade")
    sudo("aptitude install libevent-dev libsqlite3-dev redis-server supervisor python-dev python-virtualenv git")
    run("mkdir -p ~/.virtualenvs")
    with cd("~/.virtualenvs"):
        run("virtualenv coloreando")
    run("mkdir -p projects/coloreando")
    with cd('projects/coloreando'):
        run('git clone https://github.com/epochiero/coloreando.git .')


@task()
def deploy():
    with cd(env.path):
        run('git pull origin master')
        with prefix('source ../../.virtualenvs/coloreando/bin/activate'):
            run('pip install -r requirements/{}.txt'.format(env.use_settings))
            run('python manage.py syncdb --settings coloreando.settings.{}'.format(env.use_settings))
            run('kill -HUP `cat /tmp/gunicorn.pid`')
