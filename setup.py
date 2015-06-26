from __future__ import unicode_literals

from codecs import open as codecs_open
from setuptools import setup, find_packages


# Get the long description from the relevant file
with codecs_open('README.rst', encoding='utf-8') as f:
    long_description = f.read()


setup(name='osmexit',
      version='0.0.1',
      description="Determine which branches have an OSM exit",
      long_description=long_description,
      classifiers=[],
      keywords='',
      author="Jacob Wasserman",
      author_email='jwasserman@gmail.com',
      url='https://github.com/mapkin/osmexit',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      extras_require={
          'test': ['pytest'],
      },
  )
