import unittest
from unittest.mock import MagicMock, Mock, patch
import catapcore.config as cfg
import os
from catapcore.common.machine.hardware import Hardware
from catapcore.common.machine.snapshot import Snapshot

cfg.SNAPSHOT_LOCATION = "./catapcore/tests/snapshots"


class TestSnapshot(unittest.TestCase):
    def setUp(self):
        self.hardware_type = "Hardware"
        self.expected_output_path = os.path.join(
            cfg.SNAPSHOT_LOCATION,
            self.hardware_type,
        )
        return super().setUp()

    def tearDown(self):
        if os.path.exists(self.expected_output_path):
            os.removedirs(self.expected_output_path)
        return super().tearDown()

    @patch(
        "catapcore.common.machine.hardware.Hardware",
        new_callable=MagicMock(spec=Hardware),
    )
    def test_snapshot_initialisation(self, mock_hardware: Hardware):
        self.mock_snapshot_hardware = {"test-hardware": mock_hardware}
        self.snapshot = Snapshot(
            hardware=self.mock_snapshot_hardware,
            hardware_type=self.hardware_type,
        )
        self.assertDictEqual(self.snapshot._hardware, self.mock_snapshot_hardware)
        self.assertEqual(self.snapshot._hardware_type, self.hardware_type)
        self.assertEqual(
            self.snapshot._default_snapshot_location,
            self.expected_output_path,
        )
        self.assertTrue(os.path.exists(self.expected_output_path))

    @patch(
        "catapcore.common.machine.hardware.Hardware.create_snapshot", new_callable=Mock
    )
    @patch(
        "catapcore.common.machine.hardware.Hardware",
        new_callable=MagicMock(spec=Hardware),
    )
    def test_update_changes_snapshot_dictionary(
        self, mock_hardware: MagicMock, mock_create_snapshot: Mock
    ):
        mock_create_snapshot.return_value = {
            "test-hardware": {
                "test": 0.0,
                "test-2": 1.0,
                "test-3": True,
            },
        }
        self.mock_snapshot_hardware = {"test-hardware": mock_hardware}
        self.snapshot = Snapshot(
            hardware=self.mock_snapshot_hardware,
            hardware_type=self.hardware_type,
        )
        snapshot_to_update = {self.hardware_type: {}}
        self.snapshot._update(
            hardware=mock_hardware,
            snapshot=snapshot_to_update,
        )
        mock_create_snapshot.assert_called_once()
        self.assertDictEqual(
            snapshot_to_update,
            {
                self.hardware_type: {
                    "test-hardware": {
                        "test": 0.0,
                        "test-2": 1.0,
                        "test-3": True,
                    },
                },
            },
        )
