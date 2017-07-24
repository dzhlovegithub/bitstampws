from setuptools import find_packages, setup

setup(
    name='bitstampws'
    , version='0.1'
    , author='sebastian'
    , author_email='oxsoftdev@gmail.com'
    , packages=find_packages()
    , url='https://github.com/oxsoftdev/bitstampws'
    , license='LICENSE.txt'
    , install_requires=['tornado']
    , dependency_links=[
        'https://github.com/oxsoftdev/design-patterns-py/tarball/master'
    ]
)

