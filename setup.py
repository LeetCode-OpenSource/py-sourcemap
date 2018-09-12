import platform
import os
import sys

from urllib.request import urlopen

from setuptools import setup
from setuptools.command.install import install as InstallCommand


version = '0.3.13'
local_build = os.environ.get('LOCAL', 0)


with open('README.md', 'r') as f:
    long_description = f.read()


class PostInstallCommand(InstallCommand):
    """Post-installation for installation mode."""

    def run(self):
        version_tag = 'v{}'.format(version)
        url_template = 'https://github.com/LeetCode-OpenSource/py-sourcemap/releases/download/{tag}/py_sourcemap.{py_ver}-{platform}.{ext}'
        (major, minor, _) = platform.python_version_tuple()
        if major != '3' or not(minor in ['5', '6', '7']):
            raise Exception('Only python 3.5, 3.6, 3.7 are supported')
        system = platform.system()
        if system == 'Linux':
            py_version = 'cpython-{}{}m'.format(major, minor)
            usr_platform = 'x86_64-linux-gnu'
            ext = 'so'
        elif system == 'Darwin':
            py_version = 'cpython-{}{}m'.format(major, minor)
            usr_platform = 'x86_64-apple-darwin'
            ext = 'so'
        elif system == 'Windows':
            py_version = 'cp{}{}'.format(major, minor)
            # from https://docs.python.org/3/library/platform.html
            is_64bits = sys.maxsize > 2**32
            usr_platform = 'win_amd64' if is_64bits else 'win32'
            ext = 'pyd'
        else:
            raise Exception('Your system is unrecognized: {}'.format(system))
        download_url = url_template.format(tag=version_tag,
                                           py_ver=py_version,
                                           platform=usr_platform,
                                           ext=ext)
        dist = os.path.join(self.build_lib, 'py_sourcemap/py_sourcemap.so')
        if not local_build:
            with open(dist, 'wb') as f:
                built_lib = urlopen(download_url).read()
                f.write(built_lib)
        InstallCommand.run(self)


install_requires = ['wheel']
tests_require = install_requires + ['pytest']

setup(
    name='py-sourcemap',
    version=version,
    packages=['py_sourcemap'],
    description='A tiny source-map-mappings bindings for python using PyO3',
    long_description=long_description,
    long_description_content_type='text/markdown',
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
    cmdclass={
        'install': PostInstallCommand,
    },
    # rust extensions are not zip safe, just like C-extensions.
    zip_safe=False)
