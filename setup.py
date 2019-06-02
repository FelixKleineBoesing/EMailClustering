from setuptools import setup
from setuptools import find_packages


setup(name='mailcluster',
      version='0.1',
      description='Clustering of E-Mails',
      url='',
      author='Felix Kleine Bösing',
      author_email='felix.boesing@t-online.de',
      license='MIT',
      packages=["mailcluster"],
      install_requires=['pywin32', "pandas", 'numpy'],
      zip_safe=False)
