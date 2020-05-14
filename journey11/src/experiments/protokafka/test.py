import unittest
from journey11.src.experiments.protokafka.protocopy import ProtoCopy
from journey11.src.experiments.protokafka.task import Task
from journey11.src.experiments.protokafka.pb_task_pb2 import PBTask
from journey11.src.experiments.protokafka.pb_message1_pb2 import PBMessage1
from journey11.src.experiments.protokafka.message1 import Message1
from journey11.src.experiments.protokafka.state import State
from journey11.src.experiments.protokafka.pb_state_pb2 import PBState


class TestProtoKafka(unittest.TestCase):
    def test_simple_class(self):
        pc = ProtoCopy()
        pc.register(object_type=Task, proto_buf_type=PBTask)

        task = Task(task_name="Task-3142", task_id=3142)

        byte_str = pc.serialize(task)
        self.assertEqual(b'\n\tTask-3142\x10\xc6\x18', byte_str)

        task_deserialized = pc.deserialize(byte_str, Task)
        self.assertEqual(task, task_deserialized)

        return

    def test_nested_class(self):
        pc = ProtoCopy()
        pc.register(object_type=Message1, proto_buf_type=PBMessage1)

        message1 = Message1(field='Message-687',
                            state=State.S2,
                            tasks=[Task(task_name="Task-1", task_id=1), Task(task_name="Task-2", task_id=2)])

        bytestr = pc.serialize(message1)
        print(bytestr)
        return


if __name__ == "__main__":
    unittest.main()
