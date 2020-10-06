import os

import requests
from invoke import run, task


def git_describe() -> str:
    """Get an identifier for the current Git commit."""
    command = "git describe --always --dirty"
    result = run(command, hide="stdout")
    return result.stdout.strip()


def purge_cache() -> None:
    """Purge cached resources from Cloudflare."""
    token = os.environ["CLOUDFLARE_API_TOKEN"]
    zone = os.environ["CLOUDFLARE_ZONE_ID"]
    response = requests.post(
        f"https://api.cloudflare.com/client/v4/zones/{zone}/purge_cache",
        headers={"Authorization": f"Bearer {token}"},
        json={"purge_everything": True},
    )
    response.raise_for_status()


@task(
    help={
        "prod": "Deploy to production.",
        "open": "Open deployment in browser.",
    }
)
def deploy(ctx, prod=False, open=False):
    """Build and deploy the site."""
    ctx.run("zola check")

    ctx.run("zola build")

    ctx.run("fd . public -e html -x htmlmin -c {} {}")

    revision = git_describe()
    command = f"netlify deploy -m 'revision {revision}'"
    if prod:
        command += " --prod"
    if open:
        command += " --open"
    ctx.run(command)

    if prod:
        purge_cache()
