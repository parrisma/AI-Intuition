import unittest
import threading
import random
import time
from pubsub import pub
from journey11.interface.task import Task
from journey11.interface.taskpool import TaskPool
from journey11.test.task.testtask import TestTask
from journey11.lib.state import State
from journey11.lib.simpletaskpool import SimpleTaskPool


class TestTheTaskPool(unittest.TestCase):

    def test_simple(self):
        test_task1 = TestTask(effort=1, start_state=State.S0)

        task_pool = SimpleTaskPool('Task Pool 1')

        res0 = task_pool.get_task(test_task1)
        self.assertIsNone(res0)
        self.assertEqual(len(task_pool), 0)

        task_pool.add_task(test_task1)
        self.assertEqual(len(task_pool), 1)

        res1 = task_pool.get_task(test_task1)

        res2 = task_pool.get_task(test_task1)
        self.assertEqual(id(test_task1), id(res1))
        self.assertIsNone(res2)
        self.assertEqual(len(task_pool), 0)

        return

    def test_multi_task_multi_state(self):
        test_task1 = TestTask(effort=1, start_state=State.S0)
        test_task2 = TestTask(effort=1, start_state=State.S0)
        test_task3 = TestTask(effort=1, start_state=State.S1)
        test_task4 = TestTask(effort=1, start_state=State.S1)
        test_task5 = TestTask(effort=1, start_state=State.S2)

        tasks = [test_task1, test_task2, test_task3, test_task4, test_task5]

        task_pool = SimpleTaskPool('Task Pool 2')

        self.assertEqual(len(task_pool), 0)
        for t in tasks:
            res0 = task_pool.get_task(t)
            self.assertIsNone(res0)
        print(task_pool)

        i = 0
        for t in tasks:
            task_pool.add_task(t)
            i += 1
            self.assertEqual(len(task_pool), i)
        print(task_pool)

        i = 5
        for t in tasks:
            res1 = task_pool.get_task(t)
            i -= 1
            self.assertEqual(len(task_pool), i)
            self.assertEqual(id(t), id(res1))
        print(task_pool)

        for t in tasks:
            res2 = task_pool.get_task(t)
            self.assertIsNone(res2)
        return

    #
    # Threaded Test Utility Class
    #
    class TaskGetter(unittest.TestCase):
        def __init__(self,
                     name: str,
                     task_pool: TaskPool,
                     task: Task,
                     lock: threading.Event):
            super().__init__()
            self._task_pool = task_pool
            self._task = task
            self._lock = lock
            self._name = name
            return

        def __call__(self, *args, **kwargs):
            print("Getter {} waiting".format(self._name))
            self._lock.wait()
            print("Getter {} running".format(self._name))
            res = self._task_pool.get_task(self._task)
            self.assertEqual(id(self._task), id(res))
            print("Getter {} done".format(self._name))

            pass

    def test_threaded_test(self):

        task_pool = SimpleTaskPool('Task Pool 3')
        lock = threading.Event()
        lock.clear()

        # Add random tasks
        #
        states = [State.S0, State.S1, State.S2, State.S3, State.S4, State.S5, State.S5, State.S7, State.S8, State.S9]
        tasks = list()
        for i in range(100):
            t = TestTask(effort=1, start_state=random.choice(states))
            tasks.append(t)
            task_pool.add_task(t)
            self.assertEqual(len(task_pool), i + 1)

        print(task_pool)

        i = 1
        for t in tasks:
            timer_action = TestTheTaskPool.TaskGetter(str(i), task_pool, t, lock)
            i += 1
            threading.Timer(0.5 + random.random(), timer_action).start()

        lock.set()
        time.sleep(2)

        self.assertEqual(len(task_pool), 0)
        for t in tasks:
            res = task_pool.get_task(t)
            self.assertIsNone(res)

        return


if __name__ == "__main__":
    unittest.main()
