import click
from datastack.server import server
@click.group()
def main():
    pass

@main.command("run")
@click.argument("target", required=True)
@click.argument("args", nargs=-1)
@click.option('--port', nargs=1, type=int)
def run(target: str, port:int, args=None, **kwargs):
    """
    Run a python script
    """
    print(target, port)
    server.start_server(target, port)

if __name__ == '__main__':
    run('test_app.py')