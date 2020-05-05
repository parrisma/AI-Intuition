from journey11.src.experiments.protobuf.helloworld_pb2 import HelloWorld
from journey11.src.experiments.protobuf.state_pb2 import State
import journey11.src.experiments.protobuf.task_pb2 as task__pb2
import journey11.src.experiments.protobuf.complex_pb2 as complex_pb2

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

    def test_complex(self):

        num_tasks = 5

        complex_expected = complex_pb2.Complex()
        complex_expected.complex_name = "Complex-1"
        complex_expected.complex_trigger = 31415
        for i in range(num_tasks):
            task_m = complex_expected.tasks.add()
            task_m.task_name = "Task{}".format(i)
            task_m.task_id = i
        complex_expected.state = State.S2
        asbin = complex_expected.SerializeToString()

        # De-serialize
        complex_actual = complex_pb2.Complex()
        complex_actual.ParseFromString(asbin)
        self.assertTrue(complex_expected.complex_name == complex_actual.complex_name)
        self.assertTrue(complex_expected.complex_trigger == complex_actual.complex_trigger)
        self.assertTrue(complex_expected.state == complex_actual.state)
        self.assertTrue(len(complex_actual.tasks) == num_tasks)
        for n in range(num_tasks):
            self.assertTrue(complex_expected.tasks[n].task_name == complex_actual.tasks[n].task_name)
            self.assertTrue(complex_expected.tasks[n].task_id == complex_actual.tasks[n].task_id)

        return


if __name__ == "__main__":
    unittest.main()
