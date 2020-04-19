import unittest
import logging
import time
from pubsub import pub
from journey11.src.interface.ether import Ether
from journey11.src.interface.capability import Capability
from journey11.src.lib.loggingsetup import LoggingSetup
from journey11.src.main.simple.simpleether import SimpleEther
from journey11.src.main.simple.simplesrcsinkping import SimpleSrcSinkPing
from journey11.src.main.simple.simplecapability import SimpleCapability
from journey11.src.lib.capabilityregister import CapabilityRegister
from journey11.src.test.ether.dummysrcsink import DummySrcSink


class TestEther(unittest.TestCase):
    _id = 1

    NO_CAPABILITIES_REQUIRED = []

    @classmethod
    def setUpClass(cls):
        LoggingSetup()

    def setUp(self) -> None:
        logging.info("\n\n- - - - - - C A S E  {} - - - - - -\n\n".format(TestEther._id))
        TestEther._id += 1
        return

    def tearDown(self) -> None:
        pub.unsubAll()

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
                srcsink = DummySrcSink()
                ether = SimpleEther("TestEther1")

                ping = SimpleSrcSinkPing(sender_srcsink=srcsink, required_capabilities=reqd_cap)
                if i == 0:
                    ether(ping)  # Invoke as callable
                elif i == 1:
                    pub.sendMessage(topicName=ether.topic, notification=ping)  # Publish direct to Ether private topic
                else:
                    pub.sendMessage(topicName=Ether.back_plane_topic(),
                                    notification=ping)  # Publish to back plane topic

                srcsink_topics = list(x.topic for x in ether.get_srcsink_addressbook)
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
        for i in range(5):
            ethers.append(SimpleEther("TestEther{}".format(i)))

        srcsinks = list()
        for _ in range(num_diff_ping_sources):
            srcsink = DummySrcSink()
            srcsinks.append(srcsink)
            ping = SimpleSrcSinkPing(sender_srcsink=srcsink, required_capabilities=TestEther.NO_CAPABILITIES_REQUIRED, )
            # Publish to back plane topic, single message should go to all ethers on backplane.
            pub.sendMessage(topicName=Ether.back_plane_topic(), notification=ping)

        for ether in ethers:
            srcsink_topics = list(x.topic for x in ether.get_srcsink_addressbook)
            self.assertEqual(num_diff_ping_sources, len(srcsink_topics))  # Num topic = num diff ones sent
            for srcsink in srcsinks:
                self.assertTrue(srcsink.topic in srcsink_topics)  # Every ether should have every topic
        return

    def test_ether_do_pub(self):
        """
        We publish a SrcSink to the back-plane and verify that all other ethers respond with their address.
        """
        required_capabilities = [[TestEther.NO_CAPABILITIES_REQUIRED, 2],
                                 [[SimpleCapability("ArbitraryCapability")], 0]]
        for reqd_cap, expected in required_capabilities:
            ether_tx1 = SimpleEther("TestEtherTx1")  # We will publish to private topic and check it replicates
            ether_rx1 = SimpleEther("TestEtherRx1")  # We will see if it gets the replicated ping.
            ether_rx2 = SimpleEther("TestEtherRx2")  # We will see if it gets the replicated ping.
            ethers = [ether_tx1, ether_rx1, ether_rx2]

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
            srcsink_topics = list(x.topic for x in ether.get_srcsink_addressbook)

            if expected == 0:
                self.assertEqual(0, len(srcsink_topics))  # We expect all topics
                self.assertTrue(ether_rx1.topic not in srcsink_topics)  # The topic should not be in the set
                self.assertTrue(ether_rx2.topic not in srcsink_topics)  # The topic should not be in the set
            else:
                self.assertEqual(2, len(srcsink_topics))  # We expect all topics
                self.assertTrue(ether_rx1.topic in srcsink_topics)  # The topic should be in the set
                self.assertTrue(ether_rx2.topic in srcsink_topics)  # The topic should be in the set

            for ether in [ether_rx1, ether_rx2]:
                logging.info("Checking {}".format(ether.name))
                srcsink_topics = list(x.topic for x in ether.get_srcsink_addressbook)
                self.assertEqual(1, len(srcsink_topics))  # We expect a single topic only
                self.assertTrue(
                    ether_tx1.topic in srcsink_topics)  # The topic should be in the set recorded by the ether
        return


if __name__ == "__main__":
    unittest.main()