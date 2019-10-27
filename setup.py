from setuptools import setup

setup(
    name='pymesoamerica',
    version='0.1.0',
    packages=['pymesoamerica', 'pymesoamerica_maya'],
    url='',
    license='',
    author='Drew J. Sonne',
    author_email='',
    description='',
    entry_points={
        'console_scripts': [
            'mesoamerica = pymesoamerica.cli:cli',
            'pymesoamerica = pymesoamerica.cli:cli'
        ],
        'pymesoamerica': [
            'borbonicus = pymesoamerica.codices:Borbonicus',
            'borgia = pymesoamerica.codices:Borgia',
            'cospi = pymesoamerica.codices:Cospi',
            'fejéváry-mayer = pymesoamerica.codices:FejevaryMayer',
            'magliabecchiano = pymesoamerica.codices:Magliabecchiano',
            'telleriano-remensis = pymesoamerica.codices:TellerianoRemensis',
            'tonalamatl-aubin = pymesoamerica.codices:TonalamatlAubin',
            'vaticanus-3738-a = pymesoamerica.codices:Vaticanus3738A',
            'vaticanus-3773-b = pymesoamerica.codices:Vaticanus3773B',
            'dresden = pymesoamerica_maya.codices:Dresden',
        ]
    },
    install_requires=['click', 'requests', 'opencv-python'],
)
