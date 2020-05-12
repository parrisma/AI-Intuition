import unittest
from journey11.src.experiments.protokafka.protocopy import ProtoCopy
from journey11.src.experiments.protokafka.task import Task
from journey11.src.experiments.protokafka.pb_task_pb2 import PBTask


class TestProtoKafka(unittest.TestCase):
    def test_task(self):
        pc = ProtoCopy()
        pc.register(object_type=Task, proto_buf_type=PBTask)

        task = Task(task_name="Task-3142", task_id=3142)

        byte_str = pc.serialize(task)
        self.assertEqual(b'\n\tTask-3142\x10\xc6\x18', byte_str)

        task_deserialized = pc.deserialize(byte_str, Task)
        self.assertEqual(task, task_deserialized)

        return


if __name__ == "__main__":
    unittest.main()
