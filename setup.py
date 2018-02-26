import functools
import pkg_resources

from setuptools import setup, find_packages
from pip.req import parse_requirements as parse_reqs

import jeeves


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
    name='jeeves-pa',
    version='0.0.2',
    description="Jeeves is a FOSS personal assistant",
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='jeeves tts stt',
    url='https://github.com/narfman0/jeeves',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        str(req.req) for req in parse_requirements('requirements.txt')
    ],
    entry_points={
        'console_scripts': [
            'jeeves=jeeves:main'
        ],
        'jeeves.stt': [
            'att = jeeves.stt:AttSTT',
            'google = jeeves.stt:GoogleSTT',
            'sphinx = jeeves.stt:PocketSphinxSTT',
            'julius = jeeves.stt:JuliusSTT',
            'witai = jeeves.stt:WitAiSTT',
        ],
    },
    test_suite='tests',
)
