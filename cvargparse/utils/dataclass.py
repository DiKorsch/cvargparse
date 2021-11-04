import pyaml

from dataclasses import Field
from dataclasses import MISSING
from dataclasses import _is_dataclass_instance
from dataclasses import asdict
from dataclasses import dataclass
from dataclasses import fields

from cvargparse import Arg

def _set_attr(cls, attr, value):
	if attr not in cls.__dict__:
		setattr(cls, attr, value)

def get_arglist(cls_or_instance) -> list:

	arglist = []
	for field in fields(cls_or_instance):
		arglist.append(FieldWrapper(field).as_arg())

	return arglist, getattr(cls_or_instance, "group_name", None)

def as_args(instance) -> list:

	dataclass_args = []
	if not _is_dataclass_instance(instance):
		return dataclass_args

	data = asdict(instance)
	for field in fields(instance):
		key = field.name
		value = data[key]
		if value == field.default:
			continue
		dataclass_args.extend(f"--{key} {value}".split())

	return dataclass_args


def cvdataclass(cls=None, *args, repr=False, **kwargs):

	def _yaml_repr_(self) -> str:
		cls_name = type(self).__name__
		return pyaml.dump({cls_name: self.__dict__}, sort_dicts=False)

	def wrap(cls):
		if not repr:
			_set_attr(cls, "__repr__", _yaml_repr_)

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
