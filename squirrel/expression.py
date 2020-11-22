def _eval_if_expression(arg, squirrel):
    if isinstance(arg, SquirrelExpression):
        return arg.eval(squirrel)
    return arg

class SquirrelExpression:
    def __init__(self, command, args):
        self.command = command
        self.args = args

    def eval(self, squirrel):
        evaluated_args = [_eval_if_expression(arg, squirrel) for arg in self.args]
        return squirrel.run_command(self.command, evaluated_args)

    def __str__(self):
        # convert this to a string representation of the expression
        return f'SquirrelExpression(command={self.command}, args={", ".join([str(a) for a in self.args])})'

def parse_string(string):
    """
        Parses a string to a SquirrelExpression
    """
    command = ''
    buffer = ''
    args = []
    parsing_args = False
    parsing_sub_expr = False
    matched_paren_pairs = 0
    for char in string:
        if char == ' ':
            if not parsing_args and buffer:
                parsing_args = True
                command = buffer
                buffer = ''
            elif parsing_sub_expr:
                buffer += ' '
            else:
                # an arg has been parsed add to args and empty the buffer
                if buffer: # if buffer is actually empty this means we have just finished
                          # parsing a sub expr
                    args.append(buffer)
                    buffer = ''
        elif char == '(':
            if not parsing_sub_expr:
                parsing_sub_expr = True
            else:
                buffer += '('
            matched_paren_pairs += 1
        elif char == ')':
            matched_paren_pairs -= 1
            if matched_paren_pairs == 0:
                # the sub expr has ended so we can add this to args as a
                # SquirrelExpression
                parsing_sub_expr = False
                args.append(parse_string(buffer))
                buffer = ''
            else:
                buffer += ')'
        else:
            buffer += char
    if parsing_sub_expr or matched_paren_pairs != 0:
        raise RuntimeError('Unmatched parenthesis in command')
    if buffer:
        # append the last command
        args.append(buffer)
    return SquirrelExpression(command, args)
