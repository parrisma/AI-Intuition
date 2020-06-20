import unittest
import logging
import time
import threading
from typing import List
from journey11.src.interface.ether import Ether
from journey11.src.interface.capability import Capability
from journey11.src.interface.notification import Notification
from journey11.src.lib.aitrace.trace import Trace
from journey11.src.lib.capabilityregister import CapabilityRegister
from journey11.src.lib.namegen.namegen import NameGen
from journey11.src.main.simple.simpleether import SimpleEther
from journey11.src.main.simple.simplesrcsinkping import SimpleSrcSinkPing
from journey11.src.main.simple.simplecapability import SimpleCapability
from journey11.src.test.agent.dummysrcsink import DummySrcSink
from journey11.src.main.simple.simplekps import SimpleKps


class EtherListener:
    def __init__(self,
                 name: str,
                 messages: List,
                 release_after: int = None):
        self._name = name
        self._messages = messages
        self._msg_idx = 0
        self._num_rx = 0
        self._done = False
        self._release_after = release_after
        self._event = None
        if self._release_after is not None:
            self._event = threading.Event()
        return

    def __call__(self, notification: Notification):
        if self._done:
            assert "Ether Listener is done: all messages rx'ed"
            return

        Trace.log().info("Ether {} - Listener rx'ed message {}".format(self._name, str(notification)))
        self._messages.append(notification)
        self._num_rx = len(self._messages)
        if self._release_after is not None:
            Trace.log().info(
                "Ether - {} of {} messages received".format(str(len(self._messages)), str(self._release_after)))
            if self._num_rx == self._release_after:
                self._done = True
                Trace.log().info("Ether - all messages received, release Event wait")
                self._event.set()
        return

    def wait_until_all_rx(self):
        if self._num_rx is not None and self._event is not None and not self._done:
            Trace.log().info("blocking wait for all messages to be rx'ed by Consumer - id:{}".format(str(id(self))))
            self._event.wait()
            Trace.log().info("Blocking wait release, all massed rx'ed - id:{}".format(str(id(self))))
        return


class TestEther(unittest.TestCase):
    _id = 1
    _kps = SimpleKps()
    capability_1 = "Cap1"
    capability_2 = "Cap2"
    NO_CAPABILITIES_REQUIRED = []

    @classmethod
    def setUpClass(cls):
        return

    def setUp(self) -> None:
        Trace.log().info("\n\n- - - - - - C A S E  {} - - - - - -\n\n".format(TestEther._id))
        TestEther._id += 1
        return

    def tearDown(self) -> None:
        # UnSubscribe
        return

    def test_ether_capability(self):
        ether = SimpleEther("TestEther1")
        self.assertEqual(float(1),
                         Capability.equivalence_factor([SimpleCapability(CapabilityRegister.ETHER.name)],
                                                       ether.capabilities))
        return

    def test_ping_single_srcsink(self):
        """
        Test all the methods of injecting a SrcSinkPing into a single Ether entity.
        """
        # Topic should be registered even if the ether does not have a matching ping capabilities
        required_capabilities = [TestEther.NO_CAPABILITIES_REQUIRED,
                                 [SimpleCapability("ArbitraryCapability")]]
        for reqd_cap in required_capabilities:
            for i in range(3):
                srcsink = DummySrcSink("DummySrcSink-2")
                ether = SimpleEther("TestEther1")
                rx_msgs = list()
                ether_listener = EtherListener(name="Listener:{}".format(ether.name),
                                               messages=rx_msgs,
                                               release_after=1)
                ether.register_notification_callback(ether_listener)
                time.sleep(2)

                ping = SimpleSrcSinkPing(sender_srcsink=srcsink, required_capabilities=reqd_cap)
                if i == 0:
                    ether(msg=ping)  # Invoke as callable - i.e. bypass Kafka
                elif i == 1:
                    TestEther._kps.connection.publish(topic=ether.topic,
                                                      msg=ping)  # Publish direct to Ether private topic
                    ether_listener.wait_until_all_rx()
                else:
                    TestEther._kps.connection.publish(topic=Ether.back_plane_topic(),
                                                      msg=ping)  # Publish to back plane topic
                    ether_listener.wait_until_all_rx()

                srcsink_topics = list(x.topic for x in ether.get_address_book())
                self.assertEqual(1, len(srcsink_topics))  # We expect a single topic only
                self.assertTrue(srcsink.topic in srcsink_topics)  # The topic should be in the set recorded by the ether
        return

    def test_ping_back_plane(self):
        """
        Test the case where we have multiple Ether entities and multiple SrcSinkPings. We send the SrcSinkPing to
        the back-plane topic *once* but all of the Ether objects should get the ping.
        """
        num_diff_ping_sources = 10

        # Topic should be registered even if the ether does not have a matching ping capabilities
        ethers = list()
        ether_listeners = list()
        for i in range(5):
            ether = SimpleEther("TestEther{}".format(i))
            rx_msgs = list()
            ether_listener = EtherListener(name="Listener:{}".format(ether.name),
                                           messages=rx_msgs,
                                           release_after=1)
            ether_listeners.append(ether_listener)
            ether.register_notification_callback(ether_listener)
            ethers.append(ether)
        time.sleep(2)

        srcsinks = list()
        for i in range(num_diff_ping_sources):
            srcsink = DummySrcSink("DummySrcSink-{}".format(NameGen.generate_random_name()))
            srcsinks.append(srcsink)
            ping = SimpleSrcSinkPing(sender_srcsink=srcsink, required_capabilities=TestEther.NO_CAPABILITIES_REQUIRED, )
            # Publish to back plane topic, single message should go to all ethers on backplane.
            TestEther._kps.connection.publish(topic=Ether.back_plane_topic(),
                                              msg=ping)  # Publish direct to Ether private topic

        time.sleep(2)
        for listener in ether_listeners:
            listener.wait_until_all_rx()

        for ether in ethers:
            srcsink_topics = list(x.topic for x in ether.get_address_book())
            self.assertEqual(num_diff_ping_sources, len(srcsink_topics))  # Num topic = num diff ones sent
            for srcsink in srcsinks:
                self.assertTrue(srcsink.topic in srcsink_topics)  # Every ether should have every topic
        return

    def test_ether_no_capabilities(self):
        self.run_ether_do_pub([TestEther.NO_CAPABILITIES_REQUIRED, 5])
        return

    def test_ether_with_capabilities(self):
        self.run_ether_do_pub([[SimpleCapability(self.capability_1)], 3])
        return

    def run_ether_do_pub(self,
                         scenario: List):
        """
        We publish a SrcSink to the back-plane and verify that all other ethers respond with their address.
        """
        reqd_cap, expected = scenario

        ether_tx1 = SimpleEther("TestEtherTx1")  # We will publish to private topic and check it replicates
        ether_rx1 = SimpleEther("TestEtherRx1")  # We will see if it gets the replicated ping.
        ether_rx2 = SimpleEther("TestEtherRx2")  # We will see if it gets the replicated ping.
        ethers = [ether_tx1, ether_rx1, ether_rx2]

        # Force in some SrcSinks with capabilities via protected methods just for testing
        ds1 = DummySrcSink(name="DS1", capability=SimpleCapability(capability_name=self.capability_1))
        ds2 = DummySrcSink(name="DS2", capability=SimpleCapability(capability_name=self.capability_2))
        ether_rx1._update_address_book()
        ether_rx2._update_address_book()

        ping = SimpleSrcSinkPing(sender_srcsink=ether_tx1, required_capabilities=reqd_cap)

        # Pub to Private
        pub.sendMessage(topicName=Ether.back_plane_topic(),
                        notification=ping)  # Publish direct to Ether private topic
        time.sleep(1)  # Wait for 1 sec to ensure the activity time triggers.
        for ether in ethers:
            ether.stop()

        # The sender of the ping request should have all the addresses on the ether
        ether = ether_tx1
        logging.info("Checking {}".format(ether.name))
        srcsink_topics = list(x.topic for x in ether.get_address_book())

        if expected == 3:
            self.assertEqual(expected, len(srcsink_topics))  # We expect all topics
            self.assertTrue(ether_rx1.topic in srcsink_topics)
            self.assertTrue(ether_rx2.topic in srcsink_topics)
            self.assertTrue(ds1.topic in srcsink_topics)  # The SrcSink with reqd capability
        else:
            self.assertEqual(expected, len(srcsink_topics))  # We expect all topics + the tx
            self.assertTrue(ether_rx1.topic in srcsink_topics)  # The topic should be in the set
            self.assertTrue(ether_rx2.topic in srcsink_topics)  # The topic should be in the set
            self.assertTrue(ether_tx1.topic in srcsink_topics)  # The topic should be in the set
            self.assertTrue(ds1.topic in srcsink_topics)  # The SrcSink with reqd capability
            self.assertTrue(ds2.topic in srcsink_topics)  # The SrcSink with reqd capability

        for ether in ethers:
            del ether
        del ds1
        del ds2
        return


if __name__ == "__main__":
    unittest.main()
