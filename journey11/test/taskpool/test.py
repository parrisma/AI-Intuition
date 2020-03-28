import logging
import unittest
import time
import math
from pubsub import pub
from journey11.test.task.testtask import TestTask
from journey11.lib.state import State
from journey11.lib.simpletaskpool import SimpleTaskPool
from journey11.lib.simpleworkinitiate import SimpleWorkInitiate
from journey11.lib.loggingsetup import LoggingSetup
from journey11.test.agent.testagent import TestAgent


class Listener:
    _id = 0

    def __init__(self):
        self.name = str(Listener._id)
        Listener._id += 1

    def __call__(self, arg1):
        logging.info("{} Rx Msg {}".format(self.name, type(arg1)))
        return


class TestTheTaskPool(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        LoggingSetup()

    def test_scenario_runner(self):

        # [task_effort, agent_capacity, num_tasks, num_agents]
        scenarios = [[1, 1, 1, 1, State.S0, State.S1],
                     [2, 1, 1, 1, State.S0, State.S1],
                     [2, 2, 1, 1, State.S0, State.S1],
                     [2, 4, 1, 1, State.S0, State.S1],
                     [4, 2, 25, 1, State.S0, State.S1],
                     [8, 2, 33, 10, State.S0, State.S1],
                     [100, 1, 1, 1, State.S0, State.S1],
                     [1, 1, 1, 1, State.S0, State.S8],
                     [3, 2, 10, 5, State.S0, State.S8],
                     [10, 2, 500, 100, State.S0, State.S8]]

        case_num = 1
        for task_effort, agent_capacity, num_tasks, num_agents, start_state, end_state in scenarios:
            case_description \
                = "Case {}: Effort={}, Capacity={}, Tasks={}, Agents={} Start={}, End={}".format(case_num,
                                                                                                 task_effort,
                                                                                                 agent_capacity,
                                                                                                 num_tasks,
                                                                                                 num_agents,
                                                                                                 start_state,
                                                                                                 end_state)
            self.test_scenario_execute(case_description,
                                       task_effort,
                                       agent_capacity,
                                       num_tasks,
                                       num_agents,
                                       start_state,
                                       end_state)
            case_num += 1
        return

    def test_scenario_execute(self,
                              case_descr: str,
                              task_effort: int,
                              agent_capacity: int,
                              num_tasks: int,
                              num_agents: int,
                              start_state: State,
                              end_state: State) -> None:
        """
        Add a singls task to pool and then get it.
        Verify the task count on the pool at all stages and ensure that the task returned is the same as the
        task injected.
        """

        logging.info("\n* * * * * * S T A R T: {} * * * * * * \n".format(case_descr))

        TestTask.global_sync_reset()

        # Tasks: Single state transition
        TestTask.process_start_state(start_state)
        TestTask.process_end_state(end_state)

        # Init task pool
        task_pool = SimpleTaskPool('Task Pool 1')

        # Create Agents
        agents = list()
        st = start_state
        i = 1
        for es in State.range(start_state, end_state)[1:]:
            for _ in range(num_agents):
                agent = TestAgent(agent_name="Agent {}".format(i),
                                  start_state=st,
                                  end_state=es,
                                  capacity=agent_capacity)
                agents.append(agent)
                i += 1
            st = es

        # Must create all agents *before* subscription - otherwise odd effect where only last agent listens.
        for agent in agents:
            pub.subscribe(agent, topicName=task_pool.topic_for_state(agent.from_state))

        # Create tasks
        tasks = list()
        work_init = list()
        for _ in range(num_tasks):
            t = TestTask(effort=task_effort, start_state=State.S0)
            tasks.append(t)
            work_init.append(SimpleWorkInitiate(t))

        for w in work_init:
            pub.sendMessage(topicName=task_pool.topic, arg1=w)

        # Wait for all tasks to report arrival in terminal state
        TestTask.global_sync_wait()
        time.sleep(1)

        # Validate behaviours for this test case
        #
        for agent in agents:
            self.assertEqual(num_tasks, agent.num_notification)

        num_transitions = len(State.range(start_state, end_state)) - 1
        self.assertEqual(0, len(task_pool))
        for t in tasks:
            self.assertEqual(end_state, t.state)
            self.assertEqual(max(1, math.ceil(task_effort / agent_capacity) * num_transitions), t.lead_time)

        task_pool.terminate_all()

        logging.info("\n* * * * * * E N D : {} * * * * * * \n".format(case_descr))

        return


if __name__ == "__main__":
    unittest.main()
