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

	def __getitem__(cls, key):
		"""
			Redefines the "[]" operation.
		"""
		return cls.as_choices()[key.lower()]

class BaseChoiceType(Enum, metaclass=MetaBaseType):
	"""
		Enum base type. Can be used to define argument choices.
		It also enables to quickly creat, get and display the defined choices.
	"""

	@classmethod
	def as_choices(cls):
		return {e.name.lower(): e for e in cls}

	@classmethod
	def get(cls, key):
		if isinstance(key, str):
			return cls[key] if key in cls else cls.Default
		elif isinstance(key, cls):
			return key
		else:
			raise ValueError("Unknown optimizer type: \"{}\"".format(key.__class__.__name__))
