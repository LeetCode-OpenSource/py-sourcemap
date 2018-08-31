from setuptools import setup
from setuptools_rust import Binding, RustExtension

setup(name='py-sourcemap',
  version='0.1',
  rust_extensions=[RustExtension('py_sourcemap.py_sourcemap',
                                  'Cargo.toml', binding=Binding.PyO3)],
  packages=['py_sourcemap'],
  setup_requires=['setuptools_rust>=0.10.2'],
  # rust extensions are not zip safe, just like C-extensions.
  zip_safe=False
)
