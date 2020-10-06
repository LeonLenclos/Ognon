from setuptools import setup

setup(
    name='ognon',
    version='1.α',
    description='Self hosted web application for drawing 2D animation.',
    url='https://leonlenclos.github.io/Ognon/',
    author='Léon Lenclos',
    author_email='leon.lenclos@gmail.com',
    packages=['ognon', 'ognon.control', 'ognon.tests'],
    include_package_data=True,
    python_requires='>3.5',
    install_requires=[
        'Pillow',
        'pytest',
        'python-osc',
        'requests',
        'ptpython'
    ],
)
