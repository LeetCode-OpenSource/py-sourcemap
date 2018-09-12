import os

from setuptools import setup
from setuptools.command.install import install as InstallCommand

from tools.download import get_remote_binary


version = '0.4.0'
local_install = os.environ.get('LOCAL', 0)


with open('README.md', 'r') as f:
    long_description = f.read()


class PostInstallCommand(InstallCommand):
    """Post-installation for installation mode."""

    def run(self):
        if not local_install:
            dist = os.path.join(self.build_lib, 'py_sourcemap/py_sourcemap.so')
            binary_fp = get_remote_binary(version)

            with open(dist, 'wb') as f:
                f.write(binary_fp.read())

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
