from setuptools import setup
from setuptools.command.install import install

class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        '''
        Write downloading process here
        mv target .so file into `py_sourcemap/py_sourcemap.so`
        '''
        install.run(self)

install_requires = []
tests_require = install_requires + ['nose']

setup(
  name='py-sourcemap',
  version='0.1',
  packages=['py_sourcemap'],
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
  ],
  install_requires=install_requires,
  tests_require=tests_require,
  test_suite='nose.collector',
  cmdclass={
    'install': PostInstallCommand,
  },
  # rust extensions are not zip safe, just like C-extensions.
  zip_safe=False
)
