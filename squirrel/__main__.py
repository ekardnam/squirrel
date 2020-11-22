from cicada_commands import register_cicada_commands
from core_commands import register_core_commands
from file_executor import SquirrelFileExecutor
from prompt import SquirrelPrompt
from squirrel import Squirrel

import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Squirrel - A dumb scripting language based on commands to analyze Liber Primus')
    parser.add_argument('--script', type=str, default='', help='A script file to execute')
    parser.add_argument('--echo', default=False, action='store_true', help='Echo the script lines')
    args = parser.parse_args()

    interpreter = Squirrel()
    register_core_commands(interpreter)
    register_cicada_commands(interpreter)

    if args.script:
        SquirrelFileExecutor(interpreter, echo_lines=args.echo).run_file(args.script)
    else:
        SquirrelPrompt(interpreter).command_loop()
