from distutils.core import setup, find_packages

setup(
    package_dir={'':'src'},
    packages=find_packages('src'),
    name='wghelper',
    entry_points={
        'console_scripts': [
            'wghelper = wghelper.command_line:main',
        ]},
    version=0.1,
    license=MIT,
    description = "CLI tool to help solve various word games using logical and regular expressions",
    author = "Cormac O' Sullivan",
    author_email= 'cormac@cosullivan.dev',
    url = "https://github.com/ctosullivan/Word-Game-Helper",
    classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    ],
)