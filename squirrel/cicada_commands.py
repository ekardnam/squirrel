from command_checks import check_n_args
from cicada_data import liber_primus

def chapter_command(squirrel, args):
    check_n_args(args, 1)
    try:
        return liber_primus[args[0]]
    except TypeError as e:
        raise RunetimeError('Index must be integer') from e
    except IndexError as e:
        raise RuntimeError(f'No chapter {args[0]}') from e

def line_command(squirrel, args):
    check_n_args(args, 2)
    try:
        return liber_primus[args[0]].split('\n')[args[1]]
    except TypeError as e:
        raise RunetimeError('Index must be integer') from e
    except IndexError as e:
        raise RuntimeError(f'No chapter:line {args[0]}:{args[1]}') from e


def register_cicada_commands(squirrel):
    squirrel.register_command('chapter', chapter_command)
    squirrel.register_command('line', line_command)
