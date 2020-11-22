from command_checks import check_n_args

import numpy as np

def int_command(squirrel, args):
    check_n_args(args, 1)
    try:
        return int(args[0])
    except ValueError as e:
        raise RuntimeError('Expecting an integer') from e

def string_command(squirrel, args):
    return ' '.join([str(a) for a in args])

def float_command(squirrel, args):
    check_n_args(args, 1)
    try:
        return float(args[0])
    except ValueError as e:
        raise RuntimeError('Expecting a floating point') from e

def array_command(squirrel, args):
    return args

def np_array_command(squirrel, args):
    return np.array(args)

def np_command(squirrel, args):
    check_n_args(args, 1)
    return np.array(args[0])

def print_command(squirrel, args):
    check_n_args(args, 1)
    print(args[0])

def set_command(squirrel, args):
    check_n_args(args, 2)
    squirrel.set_variable(args[0], args[1])

def get_command(squirrel, args):
    check_n_args(args, 1)
    return squirrel.get_variable(args[0])

def sum_command(squirrel, args):
    accumulator = args[0]
    for arg in args[1:]:
        accumulator += arg
    return accumulator

def opp_command(squirrel, args):
    check_n_args(args, 1)
    return -args[0]

def sub_command(squirrel, args):
    check_n_args(args, 2)
    return args[0] - args[1]

def mul_command(squirrel, args):
    accumulator = args[0]
    for arg in args[1:]:
        accumulator *= arg
    return accumulator

def inv_command(squirrel, args):
    check_n_args(args, 1)
    try:
        return 1 / args[0]
    except ZeroDivisionError as e:
        raise RuntimeError('Cannot divide by zero') from e

def div_command(squirrel, args):
    check_n_args(args, 2)
    try:
        return args[0] / args[1]
    except ZeroDivisionError as e:
        raise RuntimeError('Cannot divide by zero') from e

def register_core_commands(squirrel):
    squirrel.register_command('int', int_command)
    squirrel.register_command('string', string_command)
    squirrel.register_command('float', float_command)
    squirrel.register_command('print', print_command)
    squirrel.register_command('get', get_command)
    squirrel.register_command('set', set_command)
    squirrel.register_command('sum', sum_command)
    squirrel.register_command('+', sum_command)
    squirrel.register_command('opp', opp_command)
    squirrel.register_command('-', opp_command)
    squirrel.register_command('sub', sub_command)
    squirrel.register_command('mul', mul_command)
    squirrel.register_command('*', mul_command)
    squirrel.register_command('inv', inv_command)
    squirrel.register_command('div', div_command)
    squirrel.register_command('array', array_command)
    squirrel.register_command('np', np_command)
    squirrel.register_command('np_array', np_array_command)
    squirrel.register_command('npa', np_array_command)
