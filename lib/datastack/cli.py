import click, os
from datastack.server import server


@click.group()
def main():
    pass


@main.command("run")
@click.argument("target", required=True)
@click.argument("args", nargs=-1)
@click.option("--port", nargs=1, type=int)
@click.option("--host", nargs=1)
def run(target: str, host, port: int, args=None, **kwargs):
    """
    Run a python script
    """
    file_path = os.path.realpath(__file__)
    if target == "docs":
        target = os.path.join(os.path.dirname(file_path), "docs.py")
    print(target, port)
    server.start_server(target, host, port)


if __name__ == "__main__":
    main()
