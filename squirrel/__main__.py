from data import liber_primus
from termcolor import colored
from routines import rune_to_text, text_to_rune, rune_to_gematria
import numpy


"""

	Squirrel main file



	Expressions are structured as
	<expr> = <command> [args ...]

	They can return a value or None
	An expression can take expressions ar args like the set command

	set [var_name] [expr_value]

"""

class Squirrel:
	def __init__(self):
		self.running = False
		self.command_handlers = {}
		self.variables = {}
		self.variables["chapter"] = 0
		self.variables["line"] = 0

	def register_command(self, command):
		def command_decorator(handler):
			if command in self.command_handlers:
				raise RuntimeError("Command already registered")
			else:
				self.command_handlers[command] = handler
		return command_decorator

	def is_running(self):
		return self.running

	def set_variable(self, name, value):
		self.variables[name] = value

	def get_variable(self, name):
		if name not in self.variables:
			raise RuntimeError("{} not defined".format(name))
		return self.variables[name]

	def get_all_vars(self):
		return self.variables

	def prompt(self):
		expr = input(colored("squirrel >", "red"))
		return expr

	def eval(self, expr):
		parts = expr.split(" ")
		return self.eval_parts(parts)

	def stop(self):
		self.running = False

	def eval_parts(self, parts):
		if parts[0] in self.command_handlers:
			return self.command_handlers[parts[0]](self, parts[1:])
		else:
			raise RuntimeError("Invalid command issued")

	def serve(self):
		self.running = True
		while self.running:
			expr = self.prompt()
			try:
				self.eval(expr)
			except RuntimeError as e:
				print(e)

def expect_full(array, err):
	if len(array) == 0:
		raise RuntimeError(err)

squirrel = Squirrel()

@squirrel.register_command("set")
def set_command(squirrel, args):
	if len(args) == 0:
		raise RuntimeError("Set command expects arguments")
	else:
		squirrel.set_variable(args[0], squirrel.eval_parts(args[1:]))

@squirrel.register_command("environ")
def environ_command(squirrel, args):
	vars = squirrel.get_all_vars()
	return vars

@squirrel.register_command("print")
def print_command(squirrel, args):
	expect_full(args, "Args expected")
	expression = args
	print(squirrel.eval_parts(expression))

@squirrel.register_command("string")
def string_command(squirrel, args):
	return " ".join(args)

@squirrel.register_command("int")
def int_command(squirrel, args):
	expect_full(args, "Args expected")
	try:
		val = int(args[0])
		return val
	except ValueError as e:
		raise RuntimeError("Invalid value") from e

@squirrel.register_command("exit")
def exit_command(squirrel, args):
	squirrel.stop()

@squirrel.register_command("chapter")
def chapter_command(squirrel, args):
	try:
		return liber_primus[squirrel.get_variable("chapter")]
	except TypeError as typeerr:
		raise RuntimeError("chapter variable has invalid type") from typeerr
	except IndexError as indexerr:
		raise RuntimeError("No chapter  {}".format(squirrel.get_variable("chapter"))) from indexerr

@squirrel.register_command("line")
def line_command(squirrel, args):
	chapter = squirrel.eval("chapter")
	try:
		return chapter.split("\n")[squirrel.get_variable("line")]
	except TypeError as typeerr:
		raise RuntimeError("line variable has invalid type") from typeerr
	except IndexError as indexerr:
		raise RuntimeError("No line {} in chapter {}".format(squirrel.get_variable("line"), squirrel.get_variable("chapter"))) from indexerr

@squirrel.register_command("decode")
def decode_command(squirrel, args):
	expect_full(args, "Args expected")
	runes = squirrel.eval_parts(args)
	return rune_to_text(runes)

@squirrel.register_command("runify")
def runify_command(squirrel, args):
	expect_full(args, "Args expected")
	text = squirrel.eval_parts(args)
	return text_to_rune(text)

@squirrel.register_command("get")
def get_command(squirrel, args):
	expect_full(args, "Args expected")
	return squirrel.get_variable(args[0])

@squirrel.register_command("gematria")
def gematria_command(squirrel, args):
	expect_full(args, "Args expected")
	return numpy.array(rune_to_gematria(squirrel.eval_parts(args)))

@squirrel.register_command("rotate")
def rotate_command(squirrel, args):
	expect_full(args, "Args expected")
	rotation = 0
	try:
		rotation = int(args[0])
	except ValueError as e:
		raise RuntimeError("Invalid rotation") from e
	gematria = squirrel.eval_parts(args[1:])
	return (gematria + rotation) % 29

@squirrel.register_command("invert")
def invert_command(squirrel, args):
	expect_full(args, "Args expected")
	gematria = squirrel.eval_parts(args)
	return (28 - gematria) % 29

if __name__ == "__main__":
	squirrel.serve()