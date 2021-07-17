#!/usr/bin/env python3

from typing import Dict, Any
from pathlib import Path
import setuptools

pkg = 'xpdt'
version_file = Path(pkg) / '__version__.py'
v: Dict[str, Any] = {}
exec(version_file.read_text(), v)

setuptools.setup(
    name=v['__title__'],
    version=v['__version__'],
    description=v['__description__'],
    author=v['__author__'],
    author_email=v['__author_email__'],
    package_data={
        pkg: ['py.typed'],
    },
    install_requires=[
        'jinja2',
    ],
    long_description=Path('README.md').read_text(),
    long_description_content_type="text/markdown",
    include_package_data=True,
    license=v['__license__'],
    platforms='any',
    packages=[
        pkg,
    ],
    url=v['__url__'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: POSIX',
        'Operating System :: POSIX :: Linux',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
    entry_points={
        'console_scripts': [
            f'{pkg} = {pkg}.__main__:main',
        ],
    },
)
