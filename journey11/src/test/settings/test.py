import unittest
import logging
import socket
from datetime import datetime
from journey11.src.lib.loggingsetup import LoggingSetup
from journey11.src.lib.settings import Settings
from journey11.src.lib.filestream import FileStream


class TestSettings(unittest.TestCase):
    _id = 1

    class DummyStream:
        pass

    class NoneStream:
        def __call__(self, *args, **kwargs):
            return None

    @classmethod
    def setUpClass(cls):
        LoggingSetup()

    def setUp(self) -> None:
        logging.info("\n\n- - - - - - C A S E  {} - - - - - -\n\n".format(TestSettings._id))
        TestSettings._id += 1
        return

    def tearDown(self) -> None:
        return

    def test_bad_stream(self):
        with self.assertRaises(ValueError):
            _ = Settings(None)
        return

    def test_none_stream(self):
        with self.assertRaises(ValueError):
            _ = Settings(TestSettings.NoneStream())
        return

    def test_not_callable(self):
        with self.assertRaises(ValueError):
            _ = Settings(TestSettings.DummyStream())
        return

    def test_bad_yaml(self):
        with self.assertRaises(Settings.BadYamlError):
            _ = Settings(FileStream("bad_settings.yml"))
        return

    def test_empty_yaml(self):
        with self.assertRaises(Settings.BadYamlError):
            _ = Settings(FileStream("empty_settings.yml"))
        return

    def test_wrong_tags_yaml(self):
        with self.assertRaises(Settings.BadYamlError):
            _ = Settings(FileStream("wrong_tag_settings.yml"))
        return

    def test_settings(self):
        """
        Simple test to verify that all fields are pulled back like for like
        """
        settings = Settings(FileStream("settings_test.yml"))
        self.assertEqual(settings.description, "Test Settings")
        self.assertEqual(settings.version, "1.2.3")
        self.assertEqual(settings.date, datetime.strptime("06 Jun 2020", "%d %b %Y"))
        host, port, url = settings.kafka
        self.assertEqual(host, "kafka-host-name")
        self.assertEqual(port, "3142")
        self.assertEqual(url, "https://url/file.yml")
        return

    def test_settings_current_host(self):
        """
        Test the <current-host> capability where the special marker <current-host> is replaced with the IP
        of the host on which the process is running
        """
        settings = Settings(FileStream("settings_current_host.yaml"))
        host, _, _ = settings.kafka
        current_host = socket.gethostbyname(socket.gethostname())
        self.assertEqual(host, current_host)
        return


if __name__ == "__main__":
    unittest.main()
