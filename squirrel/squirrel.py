from expression import parse_string

class Squirrel:
    """
        Squirrel is a dumb interpreted language. It basically works this way.
        Each command takes some arguments:
            [command] ...args...
        and evaluates to a value (python types)

        You can evaluate a command and use its value as a single argument
        for another command using {command} similarly to $(command) in
        bash.

        The only concept existing in Squirrel is the one of command.
        String, integer nor any other kind of literal exists. This means
        that if you wanna define a string literal you have to use the string
        command, same goes for ints.

        This design simplifies a lot the code for Squirrel but makes coding in
        Squirrel more difficult.

        As an example suppose you want to build an hello world program in Squirrel
        You gonna have to write:
            print (string hello world!)

        print is a command that takes one argument which is a string.
        string is a command that evaluates to the string obtained by concatenating
        its arguments with spaces.
        You can think of (string hello world!) as the same of "hello world!"
    """

    def __init__(self):
        self.command_handlers = {}
        self.variables_map = {}

    def register_command(self, command, handler):
        if command in self.command_handlers:
            raise ValueError('Command already registered')
        else:
            self.command_handlers[command] = handler

    def set_variable(self, name, value):
        self.variables_map[name] = value

    def get_variable(self, name):
        if name not in self.variables_map:
            raise RuntimeError(f'Variable {name} not defined')
        return self.variables_map[name]

    def run_command(self, command, args):
        if command not in self.command_handlers:
            raise RuntimeError(f'Invalid command {command}')
        return self.command_handlers[command](self, args)

    def eval_string(self, expression_string):
        # first find all the commands enclosed in () and evaluate them
        return parse_string(expression_string).eval(self)
