"""
Copyright (C) 2017 kanishka-linux kanishka.linux@gmail.com

This file is part of hlspy.

hlspy is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

hlspy is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with hlspy.  If not, see <http://www.gnu.org/licenses/>.
"""


from setuptools import setup
import os
import shutil

setup(
    name='hlspy',
    version='1.0.0',
    license='GPLv3',
    author='kanishka-linux',
    author_email='kanishka.linux@gmail.com',
    url='https://github.com/kanishka-linux/hlspy',
    long_description="README.md",
    packages=['src'],
    include_package_data=True,
    entry_points={'console_scripts':['hlspy = src.__init__:main']},
    install_requires=['PyQt5'],
    description="A simple headless browser based on QtWebEngine",
)
