from setuptools import setup, find_packages

setup(
    package_dir={'':'src'},
    packages=find_packages('src'),
    name='sbhelper',
    entry_points={
        'console_scripts': [
            'sbhelper = sbhelper.command_line:main',
        ]},
    version='0.2',
    license='MIT',
    description = "CLI tool to help solve NYTimes Spelling Bee puzzles",
    author = "Cormac O' Sullivan",
    author_email= 'cormac@cosullivan.dev',
    url = "https://github.com/ctosullivan/Spelling-Bee-Helper",
    classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    ],
)