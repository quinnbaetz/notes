import logging as log
import os
from tornado.options import define, options
import inferno.stdlib
import inferno.config


# Application defaults
if not inferno.config.is_defined('app_name'):
    define("app_name", default="notes", help="Application code name", type=str)
define("host", default=None, help="Host to bind", type=str)
define("port", default=8104, help="Port to bind", type=int)
define('root_url', default='http://localhost:8104')
define('basedir', default=inferno.stdlib.absdir(__file__))
define('static_path', default=os.path.join(inferno.stdlib.absdir(__file__), 'static'))

# MySQL
define('mysql_host', default='127.0.0.1')
define('mysql_schema', default='notes')
define('mysql_user', default='notes')
define('mysql_password', default='notes')
define('use_mysql', default=False, type=bool)

# Oracle
define('use_oracle', default=False, type=bool)

# Redis
define('use_redis', default=False, type=bool)

# Memcached
define('use_memcached', default=False, type=bool)

# Email
define('from_email', default=None)
define('to_email', default=None)
define('hostname', default='localhost')

# Auditing
define('use_audit', default=False, type=bool)

#Deploying
define('github_user', default='quinnbaetz', type=str)
define('deploy_user', default='ubuntu', type=str)

# Deployment info for fabfile setup
define('deploy_src_dir', default='/usr/local/src/notes', type=str)
define('deploy_code_dir', default='/srv/www/notes', type=str)
define('deploy_lockfile', default='/tmp/notes_deploy', type=str)
define('deploy_local', default=['localhost'], multiple=True)
define('deploy_test', default=['test01'], multiple=True)
define('deploy_dev', default=['ec2-23-22-156-53.compute-1.amazonaws.com'], multiple=True)
define('deploy_staging', default=['session01'], multiple=True)
define('deploy_prod', default=['web04', 'web05'], multiple=True)
define('deploy_upstarts', default=['tornado'], multiple=True)


# Environment settings
user = os.getenv('USER')

environments = {
    'local': {
        'from_email': 'Inferno <%s+inferno@monkeyinferno.com>' % user,
        'to_email': '%s@monkeyinferno.com' % user,
        'hostname': 'notes.local.monkeyinferno.com',
    },
    'peleus': {
        'from_email': 'Inferno <%s+inferno@monkeyinferno.com>' % user,
        'to_email': '%s@monkeyinferno.com' % user,
        'hostname': 'notes.peleus.monkeyinferno.com',
    },
    'dev': {
        'root_url': 'http://http://ec2-23-22-156-53.compute-1.amazonaws.com/',
        'hostname': 'ec2-23-22-156-53.compute-1.amazonaws.com/',
        'mysql_host': 'devdb-master',
        'from_email': 'Inferno Errors <software-errors@monkeyinferno.com>',
        'to_email': 'Inferno Errors <software-errors@monkeyinferno.com>',
    },
}
