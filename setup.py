import platform
import os
import sys

from urllib.request import urlopen

from setuptools import setup
from setuptools.command.install import install


version = '0.2.3'
local_build = os.environ.get('LOCAL', 0)


with open('README.md', 'r') as f:
    long_description = f.read()


class PostInstallCommand(install):
    """Post-installation for installation mode."""

    def run(self):
        version_tag = 'v{}'.format(version)
        url_template = 'https://github.com/LeetCode-OpenSource/py-sourcemap/releases/download/{tag}/py_sourcemap.cpython-{py_ver}-{platform}.so'
        py_version = '{}{}m'.format(sys.version_info.major,
                                    sys.version_info.minor)
        system = platform.system()
        if system == 'Linux':
            usr_platform = 'x86_64-linux-gnu'
        else:
            raise Exception('This lib is only supporting Linux for now.')
        download_url = url_template.format(tag=version_tag,
                                           py_ver=py_version,
                                           platform=usr_platform)
        dist = os.path.join(self.build_lib, 'py_sourcemap/py_sourcemap.so')
        if not local_build:
            with open(dist, 'wb') as f:
                built_lib = urlopen(download_url).read()
                f.write(built_lib)
        install.run(self)


install_requires = ['wheel']
tests_require = install_requires + ['nose']

setup(
    name='py-sourcemap',
    version=version,
    packages=['py_sourcemap'],
    description='A tiny source-map-mappings bindings for python using PyO3',
    long_description=long_description,
    url='https://github.com/LeetCode-OpenSource/py-sourcemap',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Rust',
        'License :: OSI Approved :: MIT License',
    ],
    install_requires=install_requires,
    tests_require=tests_require,
    test_suite='nose.collector',
    cmdclass={
        'install': PostInstallCommand,
    },
    # rust extensions are not zip safe, just like C-extensions.
    zip_safe=False)
