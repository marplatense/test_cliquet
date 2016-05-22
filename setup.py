import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.txt')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()

requires = [
    'kinto',
    'psycopg2',
    'pyramid',
    'pyramid_sqlalchemy',
    'pyramid_tm',
    'SQLAlchemy',
    'waitress',
    'zope.sqlalchemy',
    ]
test_requires = [
    'pytest',
    'factory_boy',
    'faker'
]

setup(name='test_cliquet',
      version='0.0',
      description='test_cliquet',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='',
      author_email='',
      url='',
      keywords='web pyramid pylons',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=test_requires,
      test_suite="tests",
      entry_points="""\
      [paste.app_factory]
      main = test_cliquet:main
      initialize = test_cliquet.scripts.initializedb:main
      """,
      )
