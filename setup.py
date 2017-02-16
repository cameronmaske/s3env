from setuptools import setup

requires = [
    'click==6.7',
    'bucketstore==0.1.1'
]


setup(
    name="s3env",
    version="0.0.4",
    author="Cameron Maske",
    description="Manipulate a key/value JSON object file in an S3 bucket through the CLI",
    author_email="cameronmaske@gmail.com",
    url='https://github.com/cameronmaske/s3env',
    py_modules=['s3env'],
    license='MIT',
    install_requires=requires,
    entry_points='''
        [console_scripts]
        s3env=s3env:cli
    ''',
)
