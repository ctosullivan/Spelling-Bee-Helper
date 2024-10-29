from setuptools import setup, find_packages

setup(
    package_dir={'':'src'},
    packages=find_packages('src'),
    name='wghelper',
    entry_points={
        'console_scripts': [
            'wghelper = wghelper.command_line:main',
        ]
    }
)