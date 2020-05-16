from . import copy

"""
Bind all handlers to the core Copy class.
"""
copy._DcopyCore.register_handler(copy._DcopyCollection)
copy._DcopyCore.register_handler(copy._DcopyEnum)
copy._DcopyCore.register_handler(copy._DcopyProto)
copy.Copy.bootstrap()
