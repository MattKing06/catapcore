from catapcore.common.machine.factory import Factory
from catapcore.common.machine.hardware import Hardware
from catapcore.common.machine.area import MachineArea
from catapcore.common.exceptions import (
    InvalidHardwareType,
    MachineAreaNotFound,
    MachineAreaNotProvided,
    HardwareNameNotFound,
    HardwareNameNotProvided,
)
import unittest
import catapcore.config as cfg

cfg.LATTICE_LOCATION = "./catapcore/tests/lattice"


class MockHardwareType(Hardware):

    def __init__(
        self,
        is_virtual: bool = False,
        connect_on_creation: bool = False,
        **kwargs,
    ):
        super().__init__(
            is_virtual=is_virtual,
            connect_on_creation=connect_on_creation,
            **kwargs,
        )


class TestFactory(unittest.TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def test_hardware_type_is_used_for_lattice_location(self):
        factory = Factory(
            is_virtual=True,
            hardware_type=MockHardwareType,
            lattice_folder="BPM",
        )
        self.assertTrue("BPM" in factory._get_config_folder())

    def test_bad_hardware_type_is_provided(self):
        with self.assertRaises(InvalidHardwareType) as error:
            Factory(
                is_virtual=True,
                hardware_type=MockHardwareType,
                lattice_folder="UNKNOWN",
            )
        self.assertEqual(
            error.exception.message,
            f"Could not find hardware type {MockHardwareType.__name__} in lattice [{cfg.LATTICE_LOCATION}/UNKNOWN].",
        )

    def test_name_exists_returns_tuple(self):
        cfg.MACHINE_AREAS = [
            MachineArea(name="BL01"),
            MachineArea(name="BL02"),
        ]
        factory = Factory(
            is_virtual=True,
            hardware_type=MockHardwareType,
            lattice_folder="BPM",
            areas=["BL01", "BL02"],
        )
        # Test return types when full hardware name exists in mapping
        self.assertIsInstance(factory._name_exists("BPM-01"), tuple)
        self.assertIsInstance(factory._name_exists("BPM-01")[0], bool)
        self.assertIsInstance(factory._name_exists("BPM-01")[1], Hardware)
        self.assertEqual(factory._name_exists("BPM-01")[0], True)
        # Test return types when hardware alias exists in mapping
        self.assertIsInstance(factory._name_exists("BL-01-BPM"), tuple)
        self.assertIsInstance(factory._name_exists("BL-01-BPM")[0], bool)
        self.assertIsInstance(factory._name_exists("BL-01-BPM")[1], Hardware)
        self.assertEqual(factory._name_exists("BL-01-BPM")[0], True)
        # Test return types when hardware does not exist in mapping
        self.assertIsInstance(factory._name_exists("NO-SUCH-BPM"), tuple)
        self.assertIsInstance(factory._name_exists("NO-SUCH-BPM")[0], bool)
        self.assertIsNone(factory._name_exists("NO-SUCH-BPM")[1], None)
        self.assertEqual(factory._name_exists("NO-SUCH-BPM")[0], False)

    def test_get_by_area_with_no_area(self):
        factory = Factory(
            is_virtual=True,
            hardware_type=MockHardwareType,
            lattice_folder="BPM",
        )
        with self.assertRaises(MachineAreaNotProvided) as error:
            factory.get_hardware_by_area(machine_areas=None, with_areas=True)
        self.assertEqual(
            error.exception.message,
            f"Please specify the machine areas you want to get {factory._hardware_type.__name__}s from.",
        )

    def test_get_by_area_with_bad_machine_area(self):
        bad_area = MachineArea(name="UNKNOWN")
        factory = Factory(
            is_virtual=True,
            hardware_type=MockHardwareType,
            lattice_folder="BPM",
        )
        with self.assertRaises(MachineAreaNotFound) as error:
            factory.get_hardware_by_area(machine_areas=bad_area, with_areas=True)
        self.assertEqual(
            error.exception.message,
            f"Could not find machine area: {bad_area.name}",
        )

    def test_get_by_area_with_bad_machine_areas(self):
        bad_areas = [
            MachineArea(name="S02"),
            MachineArea(name="UNKNOWN"),
        ]
        factory = Factory(
            is_virtual=True,
            hardware_type=MockHardwareType,
            lattice_folder="BPM",
        )
        hardware = factory.get_hardware_by_area(
            machine_areas=bad_areas, with_areas=True
        )
        self.assertNotIn("UNKNOWN", hardware.keys())

    def test_get_by_area_with_non_list(self):
        bad_type_area = {"S02": MachineArea(name="S02")}
        factory = Factory(
            is_virtual=True,
            hardware_type=MockHardwareType,
            lattice_folder="BPM",
        )
        with self.assertRaises(MachineAreaNotProvided) as error:
            factory.get_hardware_by_area(
                machine_areas=bad_type_area,
                with_areas=True,
            )
        self.assertEqual(
            error.exception.message,
            "Please provide a MachineArea or list of MachineAreas to filter by.",
        )

    def test_get_by_area_without_areas_in_resulting_dict(self):
        cfg.MACHINE_AREAS = [
            MachineArea(name="BL01"),
            MachineArea(name="BL02"),
        ]
        area = MachineArea(name="BL01")
        factory = Factory(
            is_virtual=True,
            hardware_type=MockHardwareType,
            lattice_folder="BPM",
        )
        hardware = factory.get_hardware_by_area(
            machine_areas=area,
            with_areas=False,
        )
        self.assertIsInstance(hardware, dict)
        # Check that we have not got areas as keys in dict
        self.assertTrue(area.name not in hardware.keys())

    def test_get_by_area_with_areas_in_resulting_dict(self):
        cfg.MACHINE_AREAS = [
            MachineArea(name="BL01"),
            MachineArea(name="BL02"),
        ]
        area = MachineArea(name="BL01")
        factory = Factory(
            is_virtual=True,
            hardware_type=MockHardwareType,
            lattice_folder="BPM",
        )
        hardware = factory.get_hardware_by_area(
            machine_areas=area,
        )
        self.assertIsInstance(hardware, dict)
        # Check that we have not got areas as keys in dict
        self.assertTrue(area.name in hardware.keys())

    def test_providing_area_filters_hardware(self):
        cfg.MACHINE_AREAS = [
            MachineArea(name="BL01"),
            MachineArea(name="BL02"),
        ]
        area = MachineArea(name="BL01")
        factory = Factory(
            is_virtual=True,
            hardware_type=MockHardwareType,
            lattice_folder="BPM",
            areas=area,
        )
        for _, bpm in factory.hardware.items():
            self.assertEqual(bpm.machine_area, area)

    def test_providing_areas_filters_hardware(self):
        cfg.MACHINE_AREAS = [
            MachineArea(name="BL01"),
            MachineArea(name="BL02"),
        ]
        areas = [MachineArea(name="BL01"), MachineArea(name="BL02")]
        factory = Factory(
            is_virtual=True,
            hardware_type=MockHardwareType,
            lattice_folder="BPM",
            areas=areas,
        )
        for _, bpm in factory.hardware.items():
            self.assertTrue(bpm.machine_area in areas)

    def test_get_hardware_with_no_name_provided(self):
        factory = Factory(
            is_virtual=True,
            hardware_type=MockHardwareType,
            lattice_folder="BPM",
        )
        with self.assertRaises(HardwareNameNotProvided) as error:
            factory.get_hardware()
        self.assertEqual(
            error.exception.message,
            f"Please specify {factory._hardware_type.__name__} name(s).",
        )

    def test_get_hardware_with_bad_name(self):
        factory = Factory(
            is_virtual=True,
            hardware_type=MockHardwareType,
            lattice_folder="BPM",
        )
        with self.assertRaises(HardwareNameNotFound) as error:
            factory.get_hardware(names="BAD-NAME")
        self.assertEqual(
            error.exception.message,
            f"Could not find {factory._hardware_type.__name__} with name BAD-NAME",
        )

    def test_get_hardware_with_bad_names(self):
        cfg.MACHINE_AREAS = [
            MachineArea(name="BL01"),
            MachineArea(name="BL02"),
        ]
        factory = Factory(
            is_virtual=True,
            hardware_type=MockHardwareType,
            lattice_folder="BPM",
        )
        with self.assertRaises(HardwareNameNotFound) as error:
            factory.get_hardware(names=["BPM-02", "BAD-NAME"])
        self.assertEqual(
            error.exception.message,
            f"Could not find {factory._hardware_type.__name__} with name BAD-NAME",
        )

    def test_get_hardware_with_name_that_exists(self):
        cfg.MACHINE_AREAS = [
            MachineArea(name="BL01"),
            MachineArea(name="BL02"),
        ]
        factory = Factory(
            is_virtual=True,
            hardware_type=MockHardwareType,
            lattice_folder="BPM",
        )
        magnet = factory.get_hardware("BPM-02")
        self.assertIsInstance(magnet, Hardware)

    def test_get_hardware_with_names_that_exist(self):
        names = ["BPM-01", "BPM-02"]
        cfg.MACHINE_AREAS = [
            MachineArea(name="BL01"),
            MachineArea(name="BL02"),
        ]
        factory = Factory(
            is_virtual=True,
            hardware_type=MockHardwareType,
            lattice_folder="BPM",
        )
        magnets = factory.get_hardware(names=names)
        self.assertIsInstance(magnets, dict)
        self.assertEqual(len(magnets), len(names))
