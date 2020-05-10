from typing import Type, ByteString


class ProtoCopy:

    def __init__(self):
        self._serialize_map = dict()
        self._deserialize_map = dict()
        return

    def add_target(self,
                   object_type: Type,
                   proto_buf_type: Type) -> None:
        """
        Register a target proto_buff_object for serialisation & se-serialisation
        :param object_type: The Type of object to register the proto-buff-object against
        :param proto_buf_type: The Protobuf Type that will be used for serialise / de serialise
        :return:
        """
        try:
            _ = object_type()
        except Exception as e:
            raise ValueError("{} must have initializer that can accept no arguments __init__() failed with [{}]".format(
                object_type.__name__, str(e)))
        try:
            _ = proto_buf_type()
        except Exception as e:
            raise ValueError("{} must have initializer that can accept no arguments __init__() failed with [{}]".format(
                object_type.__name__, str(e)))
        if object_type.__name__ in self._serialize_map:
            raise ValueError("Type {} is already registered".format(object_type.__name__))
        if proto_buf_type.__name__ in self._deserialize_map:
            raise ValueError("Protobuf Type {} is already registered".format(proto_buf_type.__name__))

        self._serialize_map[object_type.__name__] = proto_buf_type
        self._deserialize_map[proto_buf_type.__name__] = object_type
        return

    def serialize(self,
                  src: object) -> ByteString:
        """
        Take the given object and serialise it using it's registered protobuf partner object
        :param src: The object to be serialised
        :return:
        """
        pbt = type(src).__name__
        if pbt not in self._serialize_map:
            raise ValueError("Objects pf type {} have not registered serializer".format(pbt))
        pbt = self._serialize_map[pbt]

        tgt = pbt()

        return ByteString()
