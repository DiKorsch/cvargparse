import pyaml

from dataclasses import dataclass
from dataclasses import fields
from dataclasses import MISSING
from dataclasses import Field

from cvargparse import Arg

def cvdataclass(cls=None, *args, repr=False, **kwargs):

	def _yaml_repr_(self) -> str:
		cls_name = type(self).__name__
		return pyaml.dump({cls_name: self.__dict__}, sort_dicts=False)

	def wrap(cls):
		if not repr and "__repr__" not in cls.__dict__:
			setattr(cls, "__repr__", _yaml_repr_)
		return dataclass(cls, *args, repr=repr, **kwargs)

	# See if we're being called as @cvdataclass or @cvdataclass().
	if cls is None:
		return wrap

	return wrap(cls)

class FieldWrapper:

	def __init__(self, field: Field):
		super().__init__()
		self._field = field

	def as_arg(self) -> Arg:
		return Arg(
			self.name,
			type=self.type,
			default=self.default,
			choices=self.choices
		)

	@property
	def field(self):
		return self._field

	@property
	def name(self):
		return f"--{self.field.name}"

	@property
	def is_choice(self):
		return isinstance(self.field.type, Choices)

	@property
	def type(self):
		if self.is_choice:
			return self.field.type._type

		return self.field.type

	@property
	def default(self):

		if self.field.default == MISSING:
			return self.type()

		return self.field.default

	@property
	def choices(self):
		if not self.is_choice:
			return None

		return self.field.type._choices

def get_arglist_from_data_class(cls) -> list:
	arglist = []
	for field in fields(cls):
		arglist.append(FieldWrapper(field).as_arg())

	return arglist, getattr(cls, "group_name", None)

class Choices:

	def __init__(self, choices, type):
		self._choices = choices
		self._type = type

	def __contains__(self, value):
		return value in self._choices

	def __call__(self, *args, **kwargs):
		return self._type(*args, **kwargs)


if __name__ == '__main__':

	@cvdataclass
	class Args:
		arg1: int = 0
		arg2: int = 1

	print(Args())
