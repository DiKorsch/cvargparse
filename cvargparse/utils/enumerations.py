from enum import Enum, EnumMeta


class MetaBaseType(EnumMeta):
	"""
		MetaType for the base enumeration type.
	"""

	def __contains__(cls, item):
		"""
			Redefines the "in" operation.
		"""
		if isinstance(item, str):
			return item.lower() in cls.as_choices()
		else:
			return super(MetaBaseType, cls).__contains__(item)

class BaseType(Enum, metaclass=MetaBaseType):
	"""
		Enum base type. Can be used to define argument choices.
		It also enables to quickly creat, get and display the defined choices.
	"""

	@classmethod
	def as_choices(cls):
		return {e.name.lower(): e for e in cls}

	@classmethod
	def get(cls, key):
		key = key.lower()
		choices = cls.as_choices()
		if key in choices:
			return choices.get(key)
		elif cls.Default:
			return cls.Default
		else:
			raise KeyError('Unknown key and no default')
