import logging
import unittest
import time
import math
import random
from pubsub import pub
from journey11.src.interface.taskconsumptionpolicy import TaskConsumptionPolicy
from journey11.src.interface.capability import Capability
from journey11.src.lib.state import State
from journey11.src.main.simple.simpletaskpool import SimpleTaskPool
from journey11.src.main.simple.simpleworknotificationdo import SimpleWorkNotificationDo
from journey11.src.lib.loggingsetup import LoggingSetup
from journey11.src.lib.greedytaskconsumptionpolicy import GreedyTaskConsumptionPolicy
from journey11.src.main.simple.simpleagent import SimpleAgent
from journey11.src.lib.uniqueworkref import UniqueWorkRef
from journey11.src.main.simple.simplecapability import SimpleCapability
from journey11.src.lib.capabilityregister import CapabilityRegister
from journey11.src.main.simple.simpleworknotificationfinalise import SimpleWorkNotificationFinalise
from journey11.src.main.simple.simpleworknotificationinitiate import SimpleWorkNotificationInitiate
from journey11.src.test.task.testtask import TestTask
from journey11.src.test.agent.dummysrcsink import DummySrcSink  # Borrow this test class


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

    def tearDown(self) -> None:
        pub.unsubAll()
        return

    def test_taskpool_capabilities(self):
        task_pool = SimpleTaskPool('Task Pool 1')
        self.assertEqual(float(1),
                         Capability.equivalence_factor([SimpleCapability(CapabilityRegister.POOL.name)],
                                                       task_pool.capabilities))
        return

    def test_handlers(self):
        task_pool = SimpleTaskPool('Task Pool 1')

        TestTask.global_sync_reset()
        TestTask.process_start_state(State.S0)
        TestTask.process_end_state(State.S1)
        test_task = TestTask(effort=1, start_state=State.S0)

        uwr = UniqueWorkRef("Dummy1", "Dummy2")
        src = DummySrcSink("Source")
        orig = DummySrcSink("originator")

        scenarios = [SimpleWorkNotificationDo(uwr, test_task, orig, src),
                     SimpleWorkNotificationFinalise(uwr, test_task, orig, src)]

        try:
            for scenario in scenarios:
                task_pool(scenario)
        except Exception as e:
            self.fail("Un expected exception {}".format(str(e)))
        return

    def test_ping_cycle(self):
        scenarios = [[[SimpleCapability(str(CapabilityRegister.POOL))], 1],
                     [[], 1],
                     [[SimpleCapability(str(CapabilityRegister.AGENT))], 0],
                     [[SimpleCapability("MadeUpCapability")], 0]]

        for scenario in scenarios:
            reqd_cap, expected_notification = scenario
            logging.info("\n\nTesting Ping Cycle with capabilities [{}]\n\n".format(str(reqd_cap)))
            ping_srcsink = DummySrcSink("PingSrcSink")
            _ = SimpleTaskPool('Task Pool 1')

            ping_workref = ping_srcsink.send_ping(required_capabilities=reqd_cap)

            time.sleep(1)
            self.assertEqual(expected_notification, len(ping_srcsink.ping_notifications))
            if expected_notification > 0:
                self.assertEqual(ping_workref.id, ping_srcsink.ping_notifications[0].sender_work_ref.id)
            pub.unsubAll()
        return

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

        scenarios = [[3, 1, 5, 2, State.S0, State.S1, greedy_policy]]
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
            self.scenario_execute(case_description,
                                  task_effort,
                                  agent_capacity,
                                  num_tasks,
                                  num_agents,
                                  start_state,
                                  end_state,
                                  cons_policy)
            pub.unsubAll()
            case_num += 1
        return

    def scenario_execute(self,
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
                agent = SimpleAgent(agent_name="Agent {}".format(i),
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
        # TODO: Agent should inject work and work only done when agent is notified of all tasks being finished.
        tasks = list()
        work_init = list()
        for _ in range(num_tasks):
            task_to_do = TestTask(effort=task_effort, start_state=State.S0)
            agent_to_initiate = random.sample(population=agents, k=1)
            work_initiate = SimpleWorkNotificationInitiate(task=task_to_do, originator=agent_to_initiate)
            tasks.append([agent_to_initiate, work_initiate])

        for a, w in work_init:
            pub.sendMessage(topicName=task_pool.topic, notification=w)

        # Wait for all tasks to report arrival in terminal state
        TestTask.global_sync_wait()
        time.sleep(1)  # To run debug set to 10'000 to give you time to debug before exit.
        task_pool.terminate_all()

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
