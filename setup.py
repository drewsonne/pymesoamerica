from setuptools import setup

setup(
    name='pymesoamerica',
    version='0.1.0',
    packages=['pymesoamerica'],
    url='',
    license='',
    author='Drew J. Sonne',
    author_email='',
    description='',
    entry_points={
        'console_scripts': [
            'mesoamerica-codices = pymesoamerica.cli:codices'
        ],
        'pymesoamerica': [
            'borbonicus = pymesoamerica.codices.borbonicus:Codex'
        ]
    }
)
