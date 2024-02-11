"""
metadir

Usage:
  metadir <path>
  metadir <path> -a | --all
  metadir -h | --help
  metadir --version

Options:
  -a --all                          Does not ignore dot files
  -i --ignore                       Regex to igore
  -h --help                         Show this screen.
  --version                         Show version.

Examples:
  metadir

Help:
  For help using this tool, please open an issue on the Github repository:
  https://gitlab.com/wefindx/metadir
"""


from inspect import getmembers, isclass

from docopt import docopt

from . import __version__ as VERSION


def main():
    """Main CLI entrypoint."""
    import metadir.commands
    options = docopt(__doc__, version=VERSION)
    # print(options)

    for (k, v) in options.items():

        if options.get('<path>'):
            k = 'init'

        if hasattr(metadir.commands, k) and v:
            module = getattr(metadir.commands, k)
            metadir.commands = getmembers(module, isclass)
            command = [command[1] for command in metadir.commands if command[0] != 'Base'][0]
            command = command(options)
            command.run()
