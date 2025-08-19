from pydantic import ValidationError
from catapcore.common.machine.area import MachineArea
import unittest


class TestMachineArea(unittest.TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def test_machine_area_name(self):
        area = MachineArea(name="S02")
        self.assertEqual(area.name, "S02")

    def test_machine_name_must_be_str(self):
        bad_names = [
            True,
            0,
            1.0,
            ["X"],
            {"Y": "Z"},
            ("S02",),
        ]
        for name in bad_names:
            with self.subTest(
                name=name,
                msg=f"Expected validation error to happen as {name} is not str type",
            ):
                with self.assertRaises(ValidationError):
                    MachineArea(name=name)
