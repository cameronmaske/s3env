# S3env

Manipulate a key/value JSON object file in an S3 bucket through the CLI. Built to ease setting [remote enviroment variables with Zappa](https://github.com/Miserlou/Zappa#remote-environment-variables).

## Usage

![](tty.gif)

### Quick start.
```
$ s3env prod get
API_KEY=secret
FOO=bar

$ s3env prod set:BONJOUR=hello
Key successfully set.
Current configuration is...
API_KEY=secret
FOO=bar
BONJOUR=hello

$ s3env prod rm:BONJOIR
Key removed.
Current configuration is...
API_KEY=secret
FOO=bar
```

### Getting started.

Install via...
```
pip install s3env
```

Create an `s3env.json`.
```
{
    "prod": "s3://your-bucket-here/file-in-bucket.json"
}
````

Run commands.
```
$ s3env --help
```

## Development

After pulling down the repo locally, create a virtualenv, then install by running...
```
pip install -e .
```


## Deployment
Publish to pypi with...
```
python setup.py sdist upload -r pypi
```
