from setuptools import setup

setup(
    name='http_server',
    description='simple http server, client, and concurrent server',
    version=0.1,
    author='AJ Wohlfert and Michael Stokley',
    license='MIT',
    py_modules=['client', 'server', 'concurrent_server'],
    package_dir={'': 'src'},
    install_requires=['gevent'],
    extras_require={'test': ['pytest', 'pytest-xdist', 'tox']},
)
