from distutils.core import setup

setup(
    name="pygoqrme",
    version="0.1.0",
    author="Jonatas Baldin",
    author_email="jonatas.baldin@gmail.com",
    packages=["pygoqrme"],
    keywords="goqrme qrcode api",
    url="https://github.com/jonatasbaldin/pygoqrme/",
    description="Library for manipulating goqr.me QRCode API",
    long_description=open('README.txt').read(),
    install_requires=[
        "requests",
    ],
    classifiers=[
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Topic :: System'
    ]
)

