#  Copyright (c) 2023.

#####
class Singleton(type):
	"""
    Metaclass definition for subclasses that must be Singleton instances.

    """
	_instances = {}

	def __call__(cls, *args, **kwargs):
		# check if the instance exists - if not, create it and add it to _instances
		if cls not in cls._instances:
			cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)

		return cls._instances[cls]
