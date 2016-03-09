from setuptools import setup

setup(
    name='http_server',
    description='testing out basic socket functionality',
    version=0.1,
    author='AJ Wohlfert and Michael Stokley',
    license='MIT',
    py_modules=['client', 'server'],
    package_dir={'': 'src'},
    install_requires=[''],
    extras_require={'test': ['pytest', 'pytest-xdist', 'tox']},
)
