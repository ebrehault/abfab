from setuptools import find_packages
from setuptools import setup


try:
    README = open('README.rst').read()
except IOError:
    README = None

setup(
    name='abfab',
    version="1.0.0",
    description='Absolutely Fabulous web server',
    long_description=README,
    install_requires=[
        'guillotina'
    ],
    author='Eric BREHAULT',
    author_email='ebrehault@gmail.com',
    url='',
    packages=find_packages(exclude=['demo']),
    include_package_data=True,
    tests_require=[
        'pytest',
    ],
    extras_require={
        "test": [
            "pytest>=3.8.0,<6.1.0",
            "docker",
            "backoff",
            "psycopg2-binary",
            "pytest-asyncio<=0.13.0",
            "pytest-cov",
            "coverage>=4.0.3",
            "pytest-docker-fixtures",
            "pytest-rerunfailures<=9.0",
            "async-asgi-testclient<2.0.0",
            "openapi-spec-validator==0.2.9",
            "aiohttp>=3.0.0,<4.0.0",
            "asyncmock",
            "prometheus-client",
        ],
    },
    classifiers=[],
    entry_points={
    }
)
