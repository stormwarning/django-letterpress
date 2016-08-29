from setuptools import setup, find_packages

from letterpress import __version__

setup(
    name='letterpress',
    version=__version__,
    description='Template filters for excellent web typography.',
    long_description=open('README.md').read(),
    author='Jeff Nelson',
    author_email='rustyangel+pypi@gmail.com',
    url='https://github.com/stormwarning/django-letterpress',
    license=open('LICENSE').read(),
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    # install_requires=['lxml'],
    zip_safe=False,
    classifiers=(
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Operating System :: OS Independent',
        'Topic :: Utilities',
        'Topic :: Text Processing :: Filters',
        'Topic :: Text Processing :: Markup :: HTML',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    )
)
