from journey11.src.experiments.protobuf.helloworld_pb2 import HelloWorld
from journey11.src.experiments.protobuf.task_pb2 import Task
import journey11.src.experiments.protobuf.task_pb2 as task__pb2
import journey11.src.experiments.protobuf.complex_pb2 as complex_pb2
import journey11.src.experiments.protobuf.state_pb2 as state__pb2

import unittest


class TestProtoHelloWorld(unittest.TestCase):

    def test_simple_serialize_deserialize(self):
        hw_out = HelloWorld()
        hw_out.person_name = "Bob"
        nums = range(10)
        for n in nums:
            hw_out.tasks[str(n)] = n
        asbin = hw_out.SerializeToString()

        # De-serialize
        hw_in = HelloWorld()
        hw_in.ParseFromString(asbin)
        self.assertTrue(hw_out.person_name == hw_in.person_name)
        self.assertTrue(len(hw_in.tasks) == len(nums))
        for n in nums:
            self.assertTrue(hw_in.tasks[str(n)] == n)
        return

    def test_task_2_task(self):
        task_orig = task__pb2.Task()
        task_orig.task_name = "Task1"
        task_orig.task_id = 1

        task_copy = task__pb2.Task()
        task_copy.CopyFrom(task_orig)
        self.assertTrue(task_orig.task_name == task_copy.task_name)
        self.assertTrue(task_orig.task_id == task_copy.task_id)
        return

    def test_state_2_state(self):
        state_orig = state__pb2.State()
        state_copy = state__pb2.State()
        state_copy.CopyFrom(state_orig)
        return

    def test_complex(self):
        task_m = Task()
        task_m.task_name = "Task1"
        task_m.task_id = 1

        complex_m = complex_pb2.Complex()
        complex_m.complex_name = "Complex-1"
        complex_m.complex_trigger = 31415
        complex_m.tasks.extend([task_m])
        complex_m.complex_state.CopyFrom(state__pb2.State().S1)

        return


if __name__ == "__main__":
    unittest.main()
