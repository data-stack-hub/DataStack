import click
from datastack.server import server
@click.group()
def main():
    pass

@main.command("run")
@click.argument("target", required=True, envvar="STREAMLIT_RUN_TARGET")
@click.argument("args", nargs=-1)
def run(target: str, args=None, **kwargs):
    """
    Run a python script
    """
    print(target)
    server.start_server(target)

if __name__ == '__main__':
    run('test_app.py')