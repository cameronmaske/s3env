import click
import json
import bucketstore
import botocore


def s3env_json():
    try:
        with open("s3env.json") as f:
            return json.load(f)
    except IOError:
        raise click.ClickException("Cannot find an s3env.json")


def get_bucket_name_and_key_path(name):
    try:
        s3_path = s3env_json()[name]
    except KeyError:
        raise click.ClickException("Cannot find {} in s3env.json".format(name))

    if s3_path.startswith("s3://"):
        s3_path = s3_path.replace("s3://", "")
    return s3_path.split("/", 1)


def get_key(env):
    bucket_name, key_path = get_bucket_name_and_key_path(env)
    try:
        bucket = bucketstore.get(bucket_name)
    except ValueError:
        if click.confirm("The bucket {} does not exist, would you like to create it?".format(bucket_name)):
            try:
                bucket = bucketstore.get(bucket_name, create=True)
            except botocore.exceptions.ClientError as e:
                if (e.response["Error"]["Code"] == "BucketAlreadyExists"):
                    raise click.ClickException("The bucket {} already exists.\nIf you created this bucket, you currently credentials do not have access, else try renaming to a different bucket".format(bucket_name))
                else:
                    raise e
        else:
            return
    try:
        key = bucket.key(key_path)
        # Call the meta, will raise the error if does not exist
        key.meta
    except botocore.exceptions.ClientError as e:
        if (e.response["Error"]["Code"] == "NoSuchKey"):
            bucket.set(key_path, "{}")
            key = bucket.key(key_path)
        else:
            raise e
    return key


@click.group()
@click.argument("env")
@click.pass_context
def cli(ctx, env):
    """
    Edit an s3 json file.
    """
    ctx.obj = {
        "env": env
    }


@cli.command()
@click.pass_context
def get(ctx):
    """
    Get key/values from an s3 json file.

    \b

        s3env prod get
        s3env staging get
    """
    s3_key = get_key(ctx.obj["env"])
    key_as_json = json.loads(s3_key.get())
    if not key_as_json:
        click.echo("No key/values are currently set.")
    else:
        click.echo("Current key/values are...")
        for k, v in key_as_json.items():
            click.echo("{}={}".format(k, v))


@cli.command()
@click.argument('key')
@click.argument('value')
@click.pass_context
def set(ctx, key, value):
    """
    Set a new key/value in an s3 json file.

    \b

        s3env prod set API_KEY "secret"
        s3env prod set DATABASE_URL sqlite3://mydatabase:password:user:9200
    """
    s3_key = get_key(ctx.obj["env"])
    key_as_json = json.loads(s3_key.get())
    key_as_json[key] = value
    s3_key.set(json.dumps(key_as_json, indent=4))
    click.echo("Key successfully set.")
    click.echo("Current key/values are...")
    for k, v in key_as_json.items():
        click.echo("{}={}".format(k, v))


@cli.command()
@click.argument('key')
@click.pass_context
def rm(ctx, key):
    """
    Remove a key from an s3 json file.

    \b

        s3env prod rm API_KEY
        s3env staging rm DEBUG
    """
    s3_key = get_key(ctx.obj["env"])
    key_as_json = json.loads(s3_key.get())
    try:
        del key_as_json[key]
        click.echo("Key removed.")
    except KeyError:
        raise click.ClickException("No key set for {}".format(key))
    s3_key.set(json.dumps(key_as_json, indent=4))
    if not key_as_json:
        click.echo("No key/values are currently set.")
    else:
        click.echo("Current key/values are...")
        for k, v in key_as_json.items():
            click.echo("{}={}".format(k, v))


if __name__ == "__main__":
    cli(obj={})
