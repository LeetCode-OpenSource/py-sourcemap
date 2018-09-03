from setuptools import setup
from setuptools.command.install import install


with open("README.md", "r") as fh:
    long_description = fh.read()


class PostInstallCommand(install):
    """Post-installation for installation mode."""

    def run(self):
        '''
        Write downloading process here
        mv target .so file into `py_sourcemap/py_sourcemap.so`
        '''
        install.run(self)


install_requires = ['wheel']
tests_require = install_requires + ['nose']

setup(
    name='py-sourcemap',
    version='0.1.9',
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
