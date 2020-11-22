class SquirrelFileExecutor:
    def __init__(self, interpreter, echo_lines=False):
        self.interpreter = interpreter
        self.echo_lines = echo_lines

    def run_file(self, filename):
        with open(filename) as script_file:
            for line in script_file.readlines():
                line = line[:-1].strip(' ')
                if self.echo_lines:
                    print(f'[+] {line}')
                if not line or line.startswith('#'):
                    continue
                self.interpreter.eval_string(line)
