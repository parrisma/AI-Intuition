import unittest
from journey11.src.experiments.protokafka.protocopy import ProtoCopy
from journey11.src.experiments.protokafka.task import Task
from journey11.src.experiments.protokafka.pb_task_pb2 import PBTask


class TestProtoKafka(unittest.TestCase):
    def test_task(self):
        pc = ProtoCopy()
        pc.add_target(object_type=Task, proto_buf_type=PBTask)
        task = Task(task_name="Task-3142", task_id=3142)
        bs = pc.serialize(task)
        print(bs)
        return


if __name__ == "__main__":
    unittest.main()
