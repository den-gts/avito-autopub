from setuptools import setup, find_packages
from os.path import join, dirname

setup(
    name='avitopub',
    version='1.0.1',
    description="Avito auto publish",
    author="Denis Epifanov",
    author_email="epifanov.denis@gmail.com",
    license="MIT",
    py_modules=['avitopub'],
    script='avitopub.py',
    long_description=open(join(dirname(__file__), 'README.md')).read(),
    entry_points={
        'console_scripts':
            ['avitopub = avitopub:main']
    },
    install_requires=['grab', 'lxml'],
    keywords=['avito', ],
    platforms="all",
    classifiers=[
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: MacOS',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Communications :: Email',
        'Topic :: Utilities',],
)