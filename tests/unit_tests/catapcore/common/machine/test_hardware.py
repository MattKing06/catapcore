import os
import unittest
from ruamel.yaml import YAML
from catapcore.common.machine.hardware import Hardware
from catapcore.common.machine.area import MachineArea
from catapcore.common.exceptions import UnexpectedPVEntry
import catapcore.config as cfg

cfg.LATTICE_LOCATION = "./catapcore/tests/lattice"


class TestPVMap(unittest.TestCase):
    def setUp(self) -> None:
        self.mock_pv_map = {"TEST": "VM-TEST-01:TEST"}
        return super().setUp()


class TestHardware(unittest.TestCase):
    def setUp(self) -> None:
        self.yaml_file = os.path.join(
            cfg.LATTICE_LOCATION,
            "BPM",
            "BPM-01.yaml",
        )
        self.hardware_config = None
        with open(self.yaml_file, "r") as file:
            yaml = YAML(typ="safe")
            self.hardware_config = dict(yaml.load(file))
        cfg.MACHINE_AREAS = [
            MachineArea(name="BL01"),
            MachineArea(name="BL02"),
        ]
        return super().setUp()

    def test_load_hardware(self):
        with self.assertWarns(
            UnexpectedPVEntry,
            msg="Expected warning about all the BPM PVs",
        ):
            hardware = Hardware(
                is_virtual=True,
                connect_on_creation=False,
                **self.hardware_config,
            )
        self.assertEqual(hardware.name, "BPM-01")
        self.assertIsInstance(hardware.aliases, list)
        self.assertIsInstance(hardware.machine_area, MachineArea)
        self.assertEqual(hardware.machine_area.name, "BL01")

    def test_load_bad_machine_area(self):
        self.hardware_config["properties"]["machine_area"] = "UNKNOWN"
        with self.assertRaises(ValueError):
            with self.assertWarns(
                UnexpectedPVEntry,
                msg="Expected warning about all the camera PVs",
            ):
                Hardware(
                    is_virtual=True,
                    connect_on_creation=False,
                    **self.hardware_config,
                )
