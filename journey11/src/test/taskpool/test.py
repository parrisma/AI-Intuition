import logging
import unittest
import time
import math
from pubsub import pub
from journey11.src.interface.taskconsumptionpolicy import TaskConsumptionPolicy
from journey11.src.interface.capability import Capability
from journey11.src.lib.state import State
from journey11.src.lib.loggingsetup import LoggingSetup
from journey11.src.lib.greedytaskconsumptionpolicy import GreedyTaskConsumptionPolicy
from journey11.src.lib.uniqueworkref import UniqueWorkRef
from journey11.src.lib.capabilityregister import CapabilityRegister
from journey11.src.lib.countdownbarrier import CountDownBarrier
from journey11.src.main.simple.simplecapability import SimpleCapability
from journey11.src.main.simple.simpleagent import SimpleAgent
from journey11.src.main.simple.simpletaskpool import SimpleTaskPool
from journey11.src.main.simple.simpleworknotificationdo import SimpleWorkNotificationDo
from journey11.src.main.simple.simpleworknotificationfinalise import SimpleWorkNotificationFinalise
from journey11.src.main.simple.simpleether import SimpleEther
from journey11.src.main.simple.simpletask import SimpleTask
from journey11.src.main.simple.simpletaskfactory import SimpleTaskFactory
from journey11.src.main.simple.simpletaskgenerationpolicyoneoffbatchuniform import \
    SimpleTaskGenerationPolicyOneOffBatchUniform
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

        SimpleTask.process_start_state(State.S0)
        SimpleTask.process_end_state(State.S1)
        test_task = SimpleTask(effort=1, start_state=State.S0)

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

        _ = SimpleEther("TestEther1")

        scenarios = [[[SimpleCapability(str(CapabilityRegister.POOL))], 1],
                     [[], 1],
                     [[SimpleCapability(str(CapabilityRegister.AGENT))], 0],
                     [[SimpleCapability("MadeUpCapability")], 0]]

        for scenario in scenarios:
            reqd_cap, expected_notification = scenario
            logging.info("\n\nTesting Ping Cycle with capabilities [{}]\n\n".format(str(reqd_cap)))
            ping_srcsink = DummySrcSink("PingSrcSink")
            task_pool = SimpleTaskPool('Task Pool 1')
            time.sleep(.25)

            ping_workref = ping_srcsink.send_ping(required_capabilities=reqd_cap)

            time.sleep(1)
            self.assertEqual(expected_notification, len(ping_srcsink.ping_notifications))
            if expected_notification > 0:
                self.assertEqual(ping_workref.id, ping_srcsink.ping_notifications[0].sender_work_ref.id)
            pub.unsubAll()
            del task_pool
            del ping_srcsink
        return

    def test_discover_pool_via_ether(self):
        """
        Test that an Agent can find and maintain a link with one or more pools.
        """
        # (1) Establish Ether to provide back-plane connectivity.
        ether = SimpleEther("TestEther1")

        # (2) Create pool - Simple pool with automatically start to ping for the Ether on the back-plane topic
        task_pool = SimpleTaskPool("TestTaskPool1")

        # (3) Allow for pings to cross propagate
        time.sleep(0.75)

        # (4) Check task_pool registered it's self with the Ether & visa versa. (Address exchange)
        self.assertTrue(task_pool in ether.get_addressbook())
        self.assertTrue(ether in task_pool.get_addressbook())

        # (5) Start simple Agent, which will automatically ping ether
        agent = SimpleAgent(agent_name="Test-Agent-1",
                            start_state=State.S0,
                            end_state=State.S1,
                            capacity=1,
                            task_consumption_policy=GreedyTaskConsumptionPolicy())

        # (6) Allow for pings to cross propagate
        time.sleep(1.00)

        # Agent should now have Ether address and Pool address
        self.assertTrue(agent in ether.get_addressbook())
        self.assertTrue(ether in agent.get_addressbook())
        self.assertTrue(task_pool in agent.get_addressbook())

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

        scenarios = [[5, 1, 2, 2, State.S0, State.S1, greedy_policy]]
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

        Flow

        1. Single ether starts ( & connects to general back-plane topic)
        2. Single task pool starts
            2.1 Automatically starts pinging looking for an Ether
            2.2 Ether replies and now Task pool is known to Ether
        3. Create specified number of agents
            3.1 Agents pings for an Ether address
            3.2 Once found Ether pings for a pool address.
            3.3 Once found pool, create send Tasks & post to Pool.
        4. Agents
            4.1 Are subscribed to Status specific topics & thus RX relevent work
            4.2 Request relevant work from pool
            4.3 If Pool assigns works, then do it.
            4.4 If Task at terminal state transition, post finalise.
            4.5 If Agent RX task finalise for task for which it is origin count as done.,
        5 All
            5.1 When all agents have RX'ed task finalization, all done
        """

        logging.info("\n* * * * * * S T A R T: {} * * * * * * \n".format(case_descr))

        ether = SimpleEther("TestEther1")

        # Tasks: State global transition range for this test
        # ToDo: https://github.com/parrisma/AI-Intuition/issues/2
        SimpleTask.process_start_state(start_state)
        SimpleTask.process_end_state(end_state)

        # Init task pool
        task_pool = SimpleTaskPool('Task Pool 1')

        # Create Agents
        tasks_per_agent = math.ceil(num_tasks / num_agents)
        agents = list()
        st = start_state
        i = 1
        ctb = CountDownBarrier(len(State.range(start_state, end_state)[1:]) * num_agents)
        for es in State.range(start_state, end_state)[1:]:
            for _ in range(num_agents):
                # Create Task Factory for Agents
                task_factory = SimpleTaskFactory(start_state=State.S0,
                                                 task_gen_policy=SimpleTaskGenerationPolicyOneOffBatchUniform(
                                                     batch_size=tasks_per_agent,
                                                     effort=task_effort))

                agent = SimpleAgent(agent_name="Agent {}".format(i),
                                    start_state=st,
                                    end_state=es,
                                    capacity=agent_capacity,
                                    task_consumption_policy=cons_policy,
                                    task_factory=task_factory,
                                    trace=True,
                                    count_down_barrier=ctb)
                agents.append(agent)
                i += 1
            st = es

        # Wait for all tasks to report arrival in terminal state
        logging.info("- - - - W A I T I N G  F O R  A L L  A G E N T S - - - - - ")
        ctb.wait()
        logging.info("- - - - D O N E  W A I T I N G  - - - - - ")
        time.sleep(1)
        task_pool.terminate_all()

        # Validate behaviours for this test case
        #
        tot_tasks = 0
        for agent in agents:
            self.assertTrue(agent.tasks_initiated == agent.tasks_finalised)
            tot_tasks += agent.tasks_worked_on
        self.assertTrue(num_tasks, tot_tasks)

        num_transitions = len(State.range(start_state, end_state)) - 1
        self.assertEqual(0, len(task_pool))
        for agent in agents:
            finalised_tasks = agent.finalised_tasks()
            for t in finalised_tasks:
                self.assertTrue(t.finalised)
                self.assertEqual(end_state, t.state, "Final state check failed for task {}".format(str(t)))
                self.assertEqual(max(1, math.ceil(task_effort / agent_capacity) * num_transitions),
                                 t.lead_time,
                                 "Lead Time check failed for task {}".format(str(t)))

        logging.info("\n* * * * * * E N D : {} * * * * * * \n".format(case_descr))

        return


if __name__ == "__main__":
    unittest.main()
