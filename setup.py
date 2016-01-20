try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import pyatomlist

with open('README.rst') as readme:
    long_description = readme.read()

setup_params = dict(
    name='pyatomlist',
    version=pyatomlist.VERSION,
    description='Simple Python tool to list all atoms and their position in a MP4 file.',
    long_description=long_description,
    author='Christian Sieber, Daniel G. Taylor (for qtfaststart)',
    author_email='c.sieber@tum.de',
    url='https://github.com/csieber/pyatomlist',
    license='MIT License',
    platforms=["any"],
    provides=['pyatomlist'],
    packages=[
        'pyatomlist',
    ],
    scripts=['bin/pyatomlist'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Multimedia :: Video :: Conversion',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)

if __name__ == '__main__':
    setup(**setup_params)
