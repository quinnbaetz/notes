# Inferno version works like this:
# x - major or fundamental changes
# x.y - incompatible changes that require modifying applications
# x.y.z - features and fixes intended to work seamlessly with applications

from setuptools import setup, find_packages
import os
import ConfigParser

def read_version():
    try:
        config = ConfigParser.SafeConfigParser()
        fp = open(os.path.join(os.path.dirname(__file__), 'notes', 'version.cfg'))
        config.readfp(fp)
        return config.get("version", "version")
    except Exception, e:
        print e
        return None

setup(
    name="notes",
    version=read_version(),
    packages=find_packages(),
    author="Quinn Baetz",
    author_email="quinn@monkeyinferno.com",
    description="notes Inferno App",
    zip_safe=False,
    include_package_data=True,
    package_data={
        '': ['templates/*', 'static/*/*', 'sql/*']
        },
    entry_points={
        # Add a command here to package css/javascript
        "disutils.commands": [
            ],

        "inferno.project": [
            "notes = notes.notes"
            ]
        },
    dependency_links=[
        "http://monkeybox.monkeyinferno.com/python",
        ],
    install_requires=[
        'distribute',
        'inferno',
        ]
)
