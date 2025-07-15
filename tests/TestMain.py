# Test case
import unittest

from src.config import config
from ok.test.TaskTestCase import TaskTestCase

from src.tasks.OneTimeTask import OneTimeTask


class TestBattleBaseSerialization(TaskTestCase):
    task_class = OneTimeTask

    config = config

    def test_ocr1(self):
        # Create a BattleReport object
        self.set_image('tests/images/main.png')
        text = self.task.find_some_text_on_bottom_right()
        self.assertEqual(text[0].name, '商城')

    def test_ocr2(self):
        # Create a BattleReport object
        self.set_image('tests/images/main.png')
        text = self.task.find_some_text_with_relative_box()
        self.assertEqual(text[0].name, '招募')


if __name__ == '__main__':
    unittest.main()
