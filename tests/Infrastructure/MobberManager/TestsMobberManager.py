import os
import random
import unittest
from approvaltests import Approvals
from approvaltests.TextDiffReporter import TextDiffReporter
from Infrastructure.MobberManager import MobberManager

os.environ["APPROVALS_TEXT_DIFF_TOOL"] = "C:\\Program Files\\TortoiseSVN\\bin\\TortoiseMerge.exe"


class TestsMobberManager(unittest.TestCase):
    def test_empty_mobber_manager_has_no_items(self):
        mobber_manager = MobberManager()
        self.assertEqual(mobber_manager.mobber_count(), 0)

    def test_add_mobber_chris_has_chris(self):
        mobber_manager = MobberManager()
        mobber_manager.add_mobber("Chris")
        result = ["Chris"]
        self.assertEqual(mobber_manager.get_mobbers(), result)

    def test_add_mobber_joe_chris_has_joe_chris(self):
        mobber_manager = MobberManager()
        mobber_manager.add_mobber("Joe")
        mobber_manager.add_mobber("Chris")
        result = ["Joe", "Chris"]
        self.assertEqual(mobber_manager.get_mobbers(), result)

    def test_add_mobber_joe_chris_joe__remove_joe_has_joe_chris(self):
        mobber_manager = MobberManager()
        mobber_manager.add_mobber("Joe")
        mobber_manager.add_mobber("Chris")
        mobber_manager.add_mobber("John")
        mobber_manager.remove_mobber(2)
        result = ["Joe", "Chris"]
        self.assertEqual(mobber_manager.get_mobbers(), result)

    def test_add_4_mobbers_move_up_middle(self):
        mobber_manager = MobberManager()
        mobber_manager.add_mobber("Joe")
        mobber_manager.add_mobber("Chris")
        mobber_manager.add_mobber("Will")
        mobber_manager.add_mobber("Eric")
        mobber_manager.move_mobber_up(2)
        result = ["Joe", "Will", "Chris", "Eric"]
        self.assertEqual(mobber_manager.get_mobbers(), result)

    def test_add_4_mobbers_move_up_top(self):
        mobber_manager = MobberManager()
        mobber_manager.add_mobber("Joe")
        mobber_manager.add_mobber("Chris")
        mobber_manager.add_mobber("Will")
        mobber_manager.add_mobber("Eric")
        mobber_manager.move_mobber_up(0)
        result = ["Eric", "Chris", "Will", "Joe"]
        self.assertEqual(mobber_manager.get_mobbers(), result)

    def test_add_4_mobbers_move_down_middle(self):
        mobber_manager = MobberManager()
        mobber_manager.add_mobber("Joe")
        mobber_manager.add_mobber("Chris")
        mobber_manager.add_mobber("Will")
        mobber_manager.add_mobber("Eric")
        mobber_manager.move_mobber_down(2)
        result = ["Joe", "Chris", "Eric", "Will"]
        self.assertEqual(mobber_manager.get_mobbers(), result)

    def test_add_4_mobbers_move_down_bottom(self):
        mobber_manager = MobberManager()
        mobber_manager.add_mobber("Joe")
        mobber_manager.add_mobber("Chris")
        mobber_manager.add_mobber("Will")
        mobber_manager.add_mobber("Eric")
        mobber_manager.move_mobber_down(3)
        result = ["Eric", "Chris", "Will", "Joe"]
        self.assertEqual(mobber_manager.get_mobbers(), result)

    def test_move_down_empty(self):
        mobber_manager = MobberManager()
        mobber_manager.move_mobber_down(0)
        result = []
        self.assertEqual(mobber_manager.get_mobbers(), result)

    def test_move_up_empty(self):
        mobber_manager = MobberManager()
        mobber_manager.move_mobber_up(0)
        result = []
        self.assertEqual(mobber_manager.get_mobbers(), result)

    def test_remove_empty(self):
        mobber_manager = MobberManager()
        mobber_manager.remove_mobber(0)
        result = []
        self.assertEqual(mobber_manager.get_mobbers(), result)

    def test_clear(self):
        mobber_manager = MobberManager()
        mobber_manager.add_mobber("Joe")
        mobber_manager.add_mobber("Chris")
        mobber_manager.add_mobber("Sam")
        mobber_manager.clear()
        result = []
        self.assertEqual(mobber_manager.get_mobbers(), result)

    def test_subscribe_to_mobber_list_changes(self):
        mobber_manager = MobberManager()
        result = {"result": "Mobbers in List for Each Change\n", "increment": 0}

        def time_change_callback(mobber_list, driver_index, next_driver_index, navigator_index):
            result["increment"] += 1
            result["result"] += "Action " + result["increment"].__str__() + ":"
            for mobber_index in range(0, mobber_list.__len__()):
                result["result"] += mobber_list[mobber_index]
                if mobber_index == driver_index:
                    result["result"] += " (Current)"
                if mobber_index == next_driver_index:
                    result["result"] += " (Next)"
                if mobber_index == navigator_index:
                    result["result"] += " (Navigator)"
                result["result"] += ", "

            result["result"] += "\n"

        mobber_manager.subscribe_to_mobber_list_change(time_change_callback)

        mobber_manager.add_mobber("Joe")
        mobber_manager.add_mobber("Chris")
        mobber_manager.add_mobber("Sam")
        mobber_manager.add_mobber("John")
        mobber_manager.switch_next_driver()
        mobber_manager.add_mobber("Bill")
        mobber_manager.switch_next_driver()
        mobber_manager.switch_next_driver()
        mobber_manager.switch_next_driver()
        mobber_manager.switch_next_driver()
        mobber_manager.switch_next_driver()
        mobber_manager.remove_mobber(2)
        mobber_manager.remove_mobber(0)
        mobber_manager.switch_next_driver()
        mobber_manager.rewind_driver()
        mobber_manager.add_mobber("Seth")
        mobber_manager.rewind_driver()
        mobber_manager.rewind_driver()
        mobber_manager.rewind_driver()
        mobber_manager.move_mobber_down(0)
        mobber_manager.add_mobber("Fredrick")
        mobber_manager.move_mobber_up(2)
        mobber_manager.remove_mobber(1)
        mobber_manager.remove_mobber(0)
        mobber_manager.remove_mobber(0)

        Approvals.verify(result["result"], TextDiffReporter())

    def test_subscribe_to_mobber_list_changes_when_navigating_after_driving(self):
        mobber_manager = MobberManager(drive_after_navigating=False)
        result = {"result": "Mobbers in List for Each Change\n", "increment": 0}

        def time_change_callback(mobber_list, driver_index, next_driver_index, navigator_index):
            result["increment"] += 1
            result["result"] += "Action " + result["increment"].__str__() + ":"
            for mobber_index in range(0, mobber_list.__len__()):
                result["result"] += mobber_list[mobber_index]
                if mobber_index == driver_index:
                    result["result"] += " (Current)"
                if mobber_index == next_driver_index:
                    result["result"] += " (Next)"
                if mobber_index == navigator_index:
                    result["result"] += " (Navigator)"
                result["result"] += ", "

            result["result"] += "\n"

        mobber_manager.subscribe_to_mobber_list_change(time_change_callback)

        mobber_manager.add_mobber("Joe")
        mobber_manager.add_mobber("Chris")
        mobber_manager.add_mobber("Sam")
        mobber_manager.add_mobber("John")
        mobber_manager.switch_next_driver()
        mobber_manager.add_mobber("Bill")
        mobber_manager.switch_next_driver()
        mobber_manager.switch_next_driver()
        mobber_manager.switch_next_driver()
        mobber_manager.switch_next_driver()
        mobber_manager.switch_next_driver()
        mobber_manager.remove_mobber(2)
        mobber_manager.remove_mobber(0)
        mobber_manager.switch_next_driver()
        mobber_manager.rewind_driver()
        mobber_manager.add_mobber("Seth")
        mobber_manager.rewind_driver()
        mobber_manager.rewind_driver()
        mobber_manager.rewind_driver()
        mobber_manager.move_mobber_down(0)
        mobber_manager.add_mobber("Fredrick")
        mobber_manager.move_mobber_up(2)
        mobber_manager.remove_mobber(1)
        mobber_manager.remove_mobber(0)
        mobber_manager.remove_mobber(0)

        Approvals.verify(result["result"], TextDiffReporter())

    def test_subscribe_to_mobber_list_changes_random(self):
        random.seed(0)
        mobber_manager = MobberManager(True)
        result = {"result": "Mobbers in List for Each Change\n", "increment": 0}

        def time_change_callback(mobber_list, driver_index, next_driver_index, navigator_index):
            result["increment"] += 1
            result["result"] += "Action " + result["increment"].__str__() + ":"
            for mobber_index in range(0, mobber_list.__len__()):
                result["result"] += mobber_list[mobber_index]
                if mobber_index == driver_index:
                    result["result"] += " (Current)"
                if mobber_index == next_driver_index:
                    result["result"] += " (Next)"
                if mobber_index == navigator_index:
                    result["result"] += " (Navigator)"
                result["result"] += ", "

            result["result"] += "\n"

        mobber_manager.subscribe_to_mobber_list_change(time_change_callback)

        mobber_manager.add_mobber("Joe")
        mobber_manager.add_mobber("Chris")
        mobber_manager.add_mobber("Sam")
        mobber_manager.add_mobber("John")
        mobber_manager.switch_next_driver()
        mobber_manager.add_mobber("Bill")
        mobber_manager.switch_next_driver()
        mobber_manager.switch_next_driver()
        mobber_manager.switch_next_driver()
        mobber_manager.set_mobber_list(["Hello", "Eric", "Joe"])
        mobber_manager.switch_next_driver()
        mobber_manager.switch_next_driver()
        mobber_manager.remove_mobber(2)
        mobber_manager.remove_mobber(0)
        mobber_manager.switch_next_driver()
        mobber_manager.add_mobber("Seth")
        mobber_manager.move_mobber_down(0)
        mobber_manager.add_mobber("Fredrick")
        mobber_manager.move_mobber_up(2)
        mobber_manager.remove_mobber(1)
        mobber_manager.remove_mobber(0)
        mobber_manager.remove_mobber(0)

        Approvals.verify(result["result"], TextDiffReporter())

    def test_next_driver1_driver0_index(self):
        mobber_manager = MobberManager()
        mobber_manager.add_mobber("Joe")
        mobber_manager.add_mobber("Chris")
        result = "Next: " + str(mobber_manager.next_driver_index) + " Current: " + str(mobber_manager.current_driver_index)
        self.assertEqual(result, "Next: 1 Current: 0")

    def test_switch_next_driver0_driver1_index(self):
        mobber_manager = MobberManager()
        mobber_manager.add_mobber("Joe")
        mobber_manager.add_mobber("Chris")
        mobber_manager.switch_next_driver()
        result = "Next: " + str(mobber_manager.next_driver_index) + " Current: " + str(mobber_manager.current_driver_index)
        self.assertEqual(result, "Next: 0 Current: 1")

    def test_navigator_defaults_to_next_driver(self):
        mobber_manager = MobberManager()
        mobber_manager.add_mobber("Joe")
        mobber_manager.add_mobber("Chris")
        result = "Next: " + str(mobber_manager.next_driver_index) + " Current: " + str(mobber_manager.current_driver_index) + " Navigator: " + str(mobber_manager.navigator_index)
        self.assertEqual(result, "Next: 1 Current: 0 Navigator: 1")

    def test_navigator_moves_with_the_next_driver(self):
        mobber_manager = MobberManager()
        mobber_manager.add_mobber("Joe")
        mobber_manager.add_mobber("Chris")
        mobber_manager.switch_next_driver()
        result = "Next: " + str(mobber_manager.next_driver_index) + " Current: " + str(mobber_manager.current_driver_index) + " Navigator: " + str(mobber_manager.navigator_index)
        self.assertEqual(result, "Next: 0 Current: 1 Navigator: 0")

    def test_navigator_defaults_when_configuration_is_set(self):
        mobber_manager = MobberManager(drive_after_navigating=False)
        mobber_manager.add_mobber("Joe")
        mobber_manager.add_mobber("Chris")
        mobber_manager.add_mobber("Tracy")
        result = "Next: " + str(mobber_manager.next_driver_index) + " Current: " + str(mobber_manager.current_driver_index) + " Navigator: " + str(mobber_manager.navigator_index)
        self.assertEqual(result, "Next: 1 Current: 0 Navigator: 2")

if __name__ == '__main__':
    unittest.main()
