from setuptools import setup, find_packages
import os

version = '1.0'

setup(name='megrok.resourcemerger',
      version=version,
      description="",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        ],
      keywords='',
      author='',
      author_email='',
      url='',
      license='ZPL 2.1',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['megrok'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'megrok.resource',
          'martian',
          'slimmer',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
