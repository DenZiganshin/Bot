import unittest
import BotConfig


class BotConfigCase(unittest.TestCase):
    def test_open_empty_config(self):
        try:
            cfg = BotConfig.BotConfig("")
        except FileNotFoundError:
            self.assertEqual(True, True)
        else:
            self.assertEqual(True, False)

    def test_open_not_empty_config(self):
            cfg = BotConfig.BotConfig("tests/config/config.json")


if __name__ == '__main__':
    unittest.main()
