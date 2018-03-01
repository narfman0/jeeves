# -*- coding: utf-8 -*-
import os
import msgfmt
import setuptools
from setuptools.command.bdist_egg import bdist_egg
from distutils.command.build import build

APPNAME = 'jeeves'


class jeeves_bdist_egg(bdist_egg):
    def run(self):
        self.run_command('build_i18n')
        setuptools.command.bdist_egg.bdist_egg.run(self)


class jeeves_build_i18n(setuptools.Command):
    description = 'compile PO translations to MO files'

    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        for root, _, filenames in os.walk(os.path.dirname(__file__)):
            for po_filename in filenames:
                filename, ext = os.path.splitext(po_filename)
                if ext != '.po':
                    continue
                path = os.path.join(root, filename)
                po_path = os.extsep.join([path, 'po'])
                mo_path = os.extsep.join([path, 'mo'])
                print('compile %s -> %s' % (po_path, mo_path))
                with open(mo_path, 'wb') as f:
                    f.write(msgfmt.Msgfmt(po_path).get())


class jeeves_build(build):
    sub_commands = build.sub_commands + [
        ('build_i18n', None)
    ]


setuptools.setup(
    name='jeeves-pa',
    version='0.0.4',
    url='http://github.com/narfman0/jeeves/',
    license='MIT',

    author='Jon Robison',
    author_email='narfman0@gmail.com',

    description=(
        'Jeeves is an open source platform for developing ' +
        'always-on, voice-controlled applications.'
    ),

    install_requires=[
        'APScheduler',
        'argparse',
        'mad',
        'python-slugify',
        'pytz',
        'PyYAML',
        'requests',
    ],

    packages=[APPNAME],
    package_data={
        APPNAME: [
            'data/audio/*.wav',
            'data/locale/*.po',
            'data/locale/*.mo',
            'data/standard_phrases/*.txt',
            '../plugins/*/*/*.py',
            '../plugins/*/*/plugin.info',
            '../plugins/*/*/*.txt',
            '../plugins/*/*/locale/*.po',
            '../plugins/*/*/locale/*.mo',
            '../plugins/*/*/tests/*.py'
        ]
    },

    data_files=[
        ('share/doc/%s' % APPNAME, [
            'LICENSE.md',
            'README.md'
        ])
    ],

    entry_points={
        'console_scripts': [
            'jeeves = %s.main:main' % APPNAME,
        ],
    },

    cmdclass={
        'bdist_egg': jeeves_bdist_egg,
        'build': jeeves_build,
        'build_i18n': jeeves_build_i18n,
    },

    test_suite='tests',
)
