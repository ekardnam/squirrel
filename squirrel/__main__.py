from data import liber_primus, table
from termcolor import colored
from routines import rune_to_text, text_to_rune, rune_to_gematria, rune_frequency
import numpy
import matplotlib.pyplot as plt


class Routine:
	def __init__(self, commands):
		self.commands = commands

	def exec(self, squirrel):
		for command in self.commands:
			ret = squirrel.eval(command)
		return ret

	def __str__(self):
		return self.commands.__str__()

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
		expr = input(colored("squirrel> ", "red"))
		return expr

	def eval(self, expr):
		parts = expr.split(" ")
		return self.eval_parts(parts)

	def stop(self):
		self.running = False

	def eval_parts(self, parts):
		if parts[0].strip() in self.command_handlers:
			return self.command_handlers[parts[0].strip()](self, parts[1:])
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
	if len(args) < 2:
		raise RuntimeError("args expected")
	rotation = squirrel.get_variable(args[0])
	if type(rotation) != int:
		raise RuntimeError("integer expected")
	array = squirrel.eval_parts(args[1:])
	return (array + rotation) % 29

@squirrel.register_command("reverse")
def reverse_command(squirrel, args):
	expect_full(args, "Args expected")
	gematria = squirrel.eval_parts(args)
	return (28 - gematria) % 29

@squirrel.register_command("runefreq")
def runefreq_command(squirrel, args):
	expect_full(args, "args expected")
	runes = squirrel.eval_parts(args)
	return rune_frequency(runes)

@squirrel.register_command("plot")
def plot_command(squirrel, args):
	expect_full(args, "args expected")
	dicto = squirrel.eval_parts(args)
	plt.bar([table[rune] for rune in list(dicto.keys())], dicto.values(), color='g')

@squirrel.register_command("showplot")
def showplot_command(squirrel, args):
	plt.show()

@squirrel.register_command("saveplot")
def saveplot_command(squirrel, args):
	expect_full(args, "args expected")
	plt.savefig(str(squirrel.get_variable(args[0])))

@squirrel.register_command("routine")
def routine_command(squirrel, args):
	expect_full(args, "args expected")
	commands = [c.strip() for c in " ".join(args).split(";")]
	return Routine(commands)

@squirrel.register_command("run")
def run_command(squirrel, args):
	expect_full(args, "args expected")
	routine = squirrel.get_variable(args[0])
	if type(routine) == Routine:
		return routine.exec(squirrel)
	else:
		raise RuntimeError("Routine expected")

@squirrel.register_command("chapterwise")
def chapterwise_command(squirrel, args):
	expect_full(args, "args expected")
	for chapter in range(0, 57):
		squirrel.eval("set chapter int {}".format(chapter))
		squirrel.eval("run {}".format(args[0]))

@squirrel.register_command("closeplot")
def closeplot_command(squirrel, args):
	plt.close()

@squirrel.register_command("concat")
def concat_command(squirrel, args):
	if len(args) < 2:
		raise RuntimeError("args expected")
	return str(squirrel.get_variable(args[0])) + str(squirrel.eval_parts(args[1:]))

@squirrel.register_command("array")
def array_command(squirrel, args):
	if len(args) <= 0:
		raise RuntimeError("args expected")
	try:
		return numpy.array([int(num.strip()) for num in " ".join(args).split(",")])
	except ValueError as e:
		raise RuntimeError("int expected") from e

@squirrel.register_command("sum")
def sum_command(squirrel, args):
	if len(args) < 2:
		raise RuntimeError("args expected")
	result = squirrel.get_variable(args[0])
	if type(result) != numpy.ndarray:
		raise RuntimeError("array expected")
	result = numpy.copy(result)
	for var in args[1:]:
		array = squirrel.get_variable(var)
		if type(array) != numpy.ndarray:
			raise RuntimeError("array expected")
		if array.shape != result.shape:
			raise RunetimeError("same shape required")
		result += array
		result %= 29
	return result

@squirrel.register_command("mod")
def mod_command(squirrel, args):
	if len(args) < 2:
		raise RuntimeError("args expected")
	modulus = squirrel.get_variable(args[0])
	if type(modulus) != int:
		raise RuntimeError("int expected")
	array = squirrel.eval_parts(args[1:])
	if type(array) != numpy.ndarray:
		raise RuntimeError("array expected")
	return array % modulus

if __name__ == "__main__":
	squirrel.serve()