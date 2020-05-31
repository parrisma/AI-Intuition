from . import dccopy

"""
Bind all handlers to the core Copy class.
"""
dccopy._DcopyCore.register_handler(dccopy._DcopyCollection)
dccopy._DcopyCore.register_handler(dccopy._DcopyEnum)
dccopy._DcopyCore.register_handler(dccopy._DcopyProto)
dccopy.DCCopy.bootstrap()
