# Python Imports
import exceptions
import sys

# Extern Imports
from tornado.options import options
import fabric.api as fab
import fabric.contrib.files as fab
import fabric.colors as colors
import inferno.fabutils as inf

# Project Imports
import notes.config as config


### Main Fabric Tasks
@fab.task
def config(tag='master', rolename='dev'):
    """usage: config:TAG,ROLE <default:master,dev>"""
    inf.setup(tag, rolename)
    try:
        fab.execute(inf.check_lock)
        fab.execute(inf.create_lock)
        fab.execute(inf.provision)
        fab.execute(inf.git_checkout)
        fab.execute(inf.config_etc)
        fab.execute(inf.reload_nginx)
        fab.execute(inf.initrestart)
        fab.execute(inf.remove_lock)
    except:
        ex = sys.exc_info()
        if type(ex[1]) not in [exceptions.SystemExit, exceptions.KeyboardInterrupt]:
            fab.execute(inf.remove_lock)
        print colors.red("########################################################")
        print colors.red("#     Config Failed. Please read above for errors      #")
        print colors.red("########################################################")
        raise


@fab.task
def deploy(tag='master', rolename='dev'):
    """usage: deploy:TAG,ROLE <default:master,dev"""
    inf.setup(tag, rolename)
    try:
        fab.execute(inf.check_lock)
        fab.execute(inf.create_lock)
        fab.execute(inf.provision)
        fab.execute(inf.git_checkout)
        if tag == 'master' and rolename == 'dev':
            fab.execute(inf.initstop)
            fab.execute(inf.make_virtualenv, 'virtualenv')
            fab.execute(inf.initstart)
        else:
            fab.execute(inf.make_virtualenv, 'virtualenv')
        fab.execute(inf.minify, rolename)
        inf.confirm(msg='deploy')
        fab.execute(inf.activate_tag)
        fab.execute(inf.initrestart)
        inf.send_email()
        fab.execute(inf.remove_lock)
    except:
        ex = sys.exc_info()
        if type(ex[1]) not in [exceptions.SystemExit, exceptions.KeyboardInterrupt]:
            fab.execute(inf.remove_lock)
        print colors.red("###########################################################")
        print colors.red("#     Deployment Failed. Please read above for errors     #")
        print colors.red("###########################################################")
        raise


@fab.task
def schema(tag='master', rolename='dev', dry_run=None, create=False):
    """usage: schema:TAG,ROLE,DRY_RUN,CREATE <default:master,dev,True,False>"""
    inf.setup(tag, rolename)
    if dry_run is None:
        dry_run = {'dev': False, 'prod': True}[rolename]
    try:
        fab.env.hosts = [fab.env.hosts[0]]
        fab.execute(inf.check_lock)
        fab.execute(inf.create_lock)
        fab.execute(inf.provision)
        fab.execute(inf.git_checkout)
        fab.execute(inf.make_virtualenv, 'virtualenv_schema')
        if dry_run:
            fab.execute(inf.schema_run, dry_run, create)
            fab.execute(inf.schema_run, dry_run, create, 'audit')
        else:
            inf.confirm('apply schema from')
            fab.execute(inf.schema_run, dry_run, create)
            fab.execute(inf.schema_run, dry_run, create, 'audit')
        fab.execute(inf.remove_lock)
    except:
        ex = sys.exc_info()
        if type(ex[1]) not in [exceptions.SystemExit, exceptions.KeyboardInterrupt]:
            fab.execute(inf.remove_lock)
        print colors.red("############################################################")
        print colors.red("#     Schema Tool Failed. Please read above for errors     #")
        print colors.red("############################################################")
        raise

@fab.task
def release(version=None):
    """usage: release"""
    if version:
        inf.bump_version(version)
    else:
        version = inf.version()
    print colors.white("Making release for %s version %s" % (inf.name(),version))
    #inf.package(version) # egg not needed for inferno apps as we work from git repo (PDW: why?)
    inf.git_tag(version)
    inf.bump_version()
    fab.local("git push")
    print colors.white("###########################################################")
    print colors.white("# Version %s successfully tagged and pushed." % version)
    print colors.white("# %s version bumped and code pushed."%inf.name())
    print colors.white("# run 'fab deploy' to push to dev")
    print colors.white("###########################################################")
