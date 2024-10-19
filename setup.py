'''
setup.py for flashcardz.py
'''

from setuptools import setup

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='flashcardz',   # name people will use to pip install
    python_requires='>=3.8',
    version='0.1.0',    # PEP 440
    description='flash cards for language learners',
    long_description=long_description,
    license='GPLv3+',
    long_description_content_type='text/markdown',
    package_dir={'': 'src'},
    classifiers=[                                # https://pypi.org/classifiers/
        'Programming Language :: Python :: 3',
        'Development Status :: 4 - Beta',
        'Natural Language :: English',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Intended Audience :: Education',
        'Intended Audience :: End Users/Desktop',
        'Operating System :: OS Independent',],
    url='https://github.com/kcarlton55/flashcardz',
    author='Kenneth Edward Carlton',
    author_email='kencarlton55@gmail.com',
    entry_points={'console_scripts': ['flashcardz=flashcardz:main']},
    keywords='flash,cards,language',
    project_urls={
            "Source":'https://github.com/kcarlton55/flashcardz',
        },
)
