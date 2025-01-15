from importlib.machinery import SourceFileLoader

from setuptools import find_packages, setup

version = SourceFileLoader(
    'version', 'cuenca_validations/version.py'
).load_module()


with open('README.md', 'r') as f:
    long_description = f.read()


setup(
    name='cuenca_validations',
    version=version.__version__,
    author='Cuenca',
    author_email='dev@cuenca.com',
    description='Cuenca common validations',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/cuenca-mx/cuenca-validations',
    packages=find_packages(),
    include_package_data=True,
    package_data=dict(cuenca_validations=['py.typed']),
    python_requires='>=3.9',
    install_requires=[
        'clabe>=2.0.0',
        'pydantic[email]>=2.10.0',
        'pydantic-extra-types>=2.10.0',
        'python-dateutil>=2.9.0',
        'phonenumbers>=8.13.0',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
