import functools
import pkg_resources

from setuptools import setup, find_packages
from pip.req import parse_requirements as parse_reqs

import client as jasper


# Compatibility with older versions of pip
pip_dist = pkg_resources.get_distribution('pip')
pip_version = tuple(map(int, pip_dist.version.split('.')))

# Use a base partial that will be updated depending on the version of pip
parse_requirements = functools.partial(parse_reqs, options=None)

if pip_version >= (1, 5):
    # pip 1.5 introduced a session kwarg that is required in later versions
    from pip.download import PipSession
    parse_requirements.keywords['session'] = PipSession()


setup(
    name=jasper.__title__,
    version=jasper.__version__,
    description=jasper.__description__,
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='jasper tts stt',
    url='https://github.com/jasperproject/jasper-client',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        str(req.req) for req in parse_requirements('client/requirements.txt')
    ],
    entry_points={
        'console_scripts': [
            'jasper=jasper:main'
        ],
    },
)
