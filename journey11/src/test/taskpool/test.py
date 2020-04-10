import logging
import unittest
import time
import math
from pubsub import pub
from journey11.src.interface.taskconsumptionpolicy import TaskConsumptionPolicy
from journey11.src.lib.state import State
from journey11.src.lib.simpletaskpool import SimpleTaskPool
from journey11.src.lib.simpleworknotificationdo import SimpleWorkNotificationDo
from journey11.src.lib.loggingsetup import LoggingSetup
from journey11.src.lib.greedytaskconsumptionpolicy import GreedyTaskConsumptionPolicy
from journey11.src.test.agent.testagent import TestAgent
from journey11.src.lib.uniqueworkref import UniqueWorkRef
from journey11.src.test.task.testtask import TestTask


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
        greedy_policy = GreedyTaskConsumptionPolicy()
        scenarios = [[1, 1, 1, 1, State.S0, State.S1, greedy_policy],
                     [2, 1, 1, 1, State.S0, State.S1, greedy_policy],
                     [2, 2, 1, 1, State.S0, State.S1, greedy_policy],
                     [2, 4, 1, 1, State.S0, State.S1, greedy_policy],
                     [4, 2, 25, 1, State.S0, State.S1, greedy_policy],
                     [8, 2, 33, 10, State.S0, State.S1, greedy_policy],
                     [100, 1, 1, 1, State.S0, State.S1, greedy_policy],
                     [1, 1, 1, 1, State.S0, State.S8, greedy_policy],
                     [3, 2, 10, 5, State.S0, State.S8, greedy_policy],
                     [10, 2, 100, 10, State.S0, State.S8, greedy_policy],
                     [10, 2, 200, 50, State.S0, State.S8, greedy_policy]]

        scenarios = [[2, 1, 1, 1, State.S0, State.S1, greedy_policy]]

        case_num = 1
        for task_effort, agent_capacity, num_tasks, num_agents, start_state, end_state, cons_policy in scenarios:
            case_description \
                = "{}: Eff={}, Cap={}, Tsks={}, Agnts={} St={}, Ed={}, Cons={}".format(case_num,
                                                                                       task_effort,
                                                                                       agent_capacity,
                                                                                       num_tasks,
                                                                                       num_agents,
                                                                                       start_state,
                                                                                       end_state,
                                                                                       cons_policy)
            self.test_scenario_execute(case_description,
                                       task_effort,
                                       agent_capacity,
                                       num_tasks,
                                       num_agents,
                                       start_state,
                                       end_state,
                                       cons_policy)
            case_num += 1
        return

    def test_scenario_execute(self,
                              case_descr: str,
                              task_effort: int,
                              agent_capacity: int,
                              num_tasks: int,
                              num_agents: int,
                              start_state: State,
                              end_state: State,
                              cons_policy: TaskConsumptionPolicy) -> None:
        """
        Execute the given scenario and then verify Agent & Task completion status is consistent with scenario
        parameters.
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
                                  capacity=agent_capacity,
                                  task_consumption_policy=cons_policy)
                agents.append(agent)
                i += 1
            st = es

        # Must create all agents *before* subscription - otherwise odd effect where only last agent listens.
        for agent in agents:
            pub.subscribe(agent, topicName=task_pool.topic_for_state(agent.from_state))

        # Create tasks
        # TODO: Agent should inject work and work only done when agent is notified of all tasks being finsihed.
        tasks = list()
        work_init = list()
        for _ in range(num_tasks):
            t = TestTask(effort=task_effort, start_state=State.S0)
            tasks.append(t)
            work_originator = agents[0]
            work_init.append(SimpleWorkNotificationDo(unique_work_ref=UniqueWorkRef(work_item_ref=work_originator.name,
                                                                                    subject_name=str(t.id)),
                                                      task=t,
                                                      originator=work_originator,
                                                      source=work_originator))

        for w in work_init:
            pub.sendMessage(topicName=task_pool.topic, notification=w)

        # Wait for all tasks to report arrival in terminal state
        TestTask.global_sync_wait()
        task_pool.terminate_all()
        time.sleep(2)

        # Validate behaviours for this test case
        #
        for agent in agents:
            self.assertEqual(num_tasks, agent.num_notification,
                             "Notification Check failed for agent {}".format(str(agent)))

        num_transitions = len(State.range(start_state, end_state)) - 1
        self.assertEqual(0, len(task_pool))
        for t in tasks:
            self.assertTrue(t.finalised)
            self.assertEqual(end_state, t.state, "Final state check failed for task {}".format(str(t)))
            self.assertEqual(max(1, math.ceil(task_effort / agent_capacity) * num_transitions),
                             t.lead_time,
                             "Lead Time check failed for task {}".format(str(t)))

        logging.info("\n* * * * * * E N D : {} * * * * * * \n".format(case_descr))

        return


if __name__ == "__main__":
    unittest.main()
