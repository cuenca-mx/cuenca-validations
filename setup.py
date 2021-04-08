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
    python_requires='>=3.6',
    install_requires=[
        'clabe>=1.2,<1.3',
        'pydantic>=1.6,<1.9',
        'dataclasses>=0.6;python_version<"3.7"',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
