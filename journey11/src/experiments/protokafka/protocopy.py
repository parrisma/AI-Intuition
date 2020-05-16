from typing import Type
from journey11.src.lib.dcopy.copy import Copy


class ProtoCopy:
    _OBJECT_TYPE = 0
    _PROTOBUF_TYPE = 1

    def __init__(self):
        self._transform_map = dict()
        return

    def register(self,
                 object_type: Type,
                 proto_buf_type: Type) -> None:
        """
        Register a target proto_buff_object for serialisation & se-serialisation
        :param object_type: The Type of object to register the proto-buff-object against
        :param proto_buf_type: The Protobuf Type that will be used for serialise / de serialise
        Note: The member names in both objects must be **identical**. In addition if you shadow the member with
              a property and name the protobuf field the same as the property the process will fails as it
              used setarttr() which does not work on a property.
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
        if object_type.__name__ in self._transform_map:
            raise ValueError("Type {} is already registered".format(object_type.__name__))

        self._transform_map[object_type.__name__] = (object_type, proto_buf_type)
        return

    def serialize(self,
                  src: object) -> bytes:
        """
        Take the given object and serialise it using it's registered protobuf partner object
        :param src: The object to be serialised. The object type must have been registered with
        its protobuf partner.
        :return:
        """
        obj_type = type(src).__name__
        if obj_type not in self._transform_map:
            raise ValueError("Object of type {} has no registered serializer".format(obj_type))
        tgt = Copy.deep_corresponding_copy(src=src, tgt=self._transform_map[obj_type][ProtoCopy._PROTOBUF_TYPE]())
        return tgt.SerializeToString()

    def deserialize(self,
                    serialized_src: bytes,
                    target_type: Type) -> object:
        """
        Take the given ByteString and deserialize it as the given type
        :param serialized_src: The required object as a ByteString
        :param target_type: The type of object to deserialize as. This must have been registered() with it't
        protobuf partner.
        :return:
        """
        if serialized_src is None or len(serialized_src) == 0 or not isinstance(serialized_src, bytes):
            raise ValueError("serialized_src must be a non zero length ByteString")
        obj_type = target_type.__name__
        if obj_type not in self._transform_map:
            raise ValueError("Object of type {} has no registered deserializer".format(target_type))
        pbt = self._transform_map[obj_type][ProtoCopy._PROTOBUF_TYPE]()
        tgt = self._transform_map[obj_type][ProtoCopy._OBJECT_TYPE]()
        pbt.ParseFromString(serialized_src)
        tgt = Copy.deep_corresponding_copy(src=pbt, tgt=tgt)
        return tgt
