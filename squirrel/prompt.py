from termcolor import colored

class SquirrelPrompt:
    def __init__(self, interpreter):
        self.interpreter = interpreter

    def prompt(self):
        expr = input(colored('[ squirrel ] ', 'red'))
        return expr

    def command_loop(self):
        while True:
            expr = self.prompt()
            if expr == 'exit' or expr == 'quit':
                break
            if expr.strip() == '':
                continue
            try:
                self.interpreter.eval_string(expr)
            except RuntimeError as e:
                print(e)
