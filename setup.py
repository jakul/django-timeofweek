from setuptools import setup, find_packages

setup(
    name='django-timeofweek',
    version='0.0.1-dev',
    description='A constructo to hold info on periods of time during a week',
    long_description=open('README.rst').read(),
    author='Craig Blaszczyk',
    author_email='masterjakul@gmail.com',
    url='https://github.com/jakul/django-timeofweek',
    download_url='https://github.com/jakul/django-timeofweek/downloads',
    license='BSD',
    packages=find_packages(exclude=('ez_setup', 'tests', 'example')),
    tests_require=[
        'django>=1.2,<1.4',
    ],
    include_package_data=True,
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)