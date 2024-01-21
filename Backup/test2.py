import unittest
from tools import AbstractTool, CommandTool

class MockTool(AbstractTool):
    def _use_tool(self):
        pass

class TestAbstractTool(unittest.TestCase):
    def test_object_id(self):
        tool = MockTool()
        self.assertEqual(len(tool.object_id), 64)  # SHA-256 hash length

    def test_use(self):
        with self.assertRaises(NotImplementedError):
            tool = MockTool()
            tool.use()

class TestCommandTool(unittest.TestCase):
    def test_command_success(self):
        tool = CommandTool("echo Hello, World!")
        self.assertEqual(tool.use(), "Output: Hello, World!")

    def test_command_error(self):
        tool = CommandTool("nonexistentcommand")
        self.assertTrue("Error occurred:" in tool.use())

if __name__ == '__main__':
    unittest.main()