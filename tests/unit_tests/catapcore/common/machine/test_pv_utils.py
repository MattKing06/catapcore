import unittest
from unittest.mock import MagicMock

from catapcore.common.exceptions import FailedEPICSOperationWarning
from catapcore.common.machine.protocol import CA, PVA
from catapcore.common.machine.pv_utils import (
    BinaryPV,
    PVSignal,
    ScalarPV,
    StatePV,
    StringPV,
)


class TestPVSignal(unittest.TestCase):
    def setUp(self):
        self.name = "TEST-PV-1"
        self.signal = PVSignal(name=self.name, protocol="CA", read_only=False)
        self.signal._pv = MagicMock()

    def test_protocol(self):
        expected_protocols = [("CA", CA), ("PVA", PVA), ("ca", CA), ("pva", PVA)]
        for i, (proto_name, protocol) in enumerate(expected_protocols):
            with self.subTest(i=i):
                signal = PVSignal(name=self.name, protocol=proto_name)
                self.assertIsInstance(signal._pv, protocol)

    def test_put(self):
        self.signal.put(value=5)
        self.signal._pv.put.assert_called_once_with(5)

    def test_put_read_only(self):
        signal = PVSignal(name=self.name, protocol="CA", read_only=True)
        with self.assertWarns(FailedEPICSOperationWarning) as w:
            signal.put(value=5.0)
            self.assertTrue("read-only" in str(w.warnings[0].message))


class TestScalarPV(unittest.TestCase):
    def setUp(self):
        self.name = "TEST-PV-1"
        self.signal = ScalarPV(name=self.name, protocol="CA", read_only=False)
        self.signal._pv = MagicMock()

    def test_get(self):
        expected_values = [5, 5.5]
        for i, expected_val in enumerate(expected_values):
            with self.subTest(i=i):
                self.signal._pv.get = MagicMock(return_value=expected_val)

                result = self.signal.get()

                self.assertEqual(result, expected_val)

    def test_get_bad_values(self):
        bad_values = [
            "test",
            [1, 2, 3],
        ]  # NOTE bool (False/True) doesn't raise this warning
        for i, expected_val in enumerate(bad_values):
            with self.subTest(i=i):
                self.signal._pv.get = MagicMock(return_value=expected_val)

                with self.assertWarns(FailedEPICSOperationWarning) as w:
                    self.signal.get()

                self.assertTrue(str(type(expected_val)) in str(w.warnings[0].message))

    def test_put(self):
        good_values = [5, 5.5]
        for i, val in enumerate(good_values):
            self.signal._pv.put.reset_mock()
            with self.subTest(i=i):
                self.signal.put(val)
                self.signal._pv.put.assert_called_once_with(val)

    def test_bad_put(self):
        bad_values = [
            "test",
            [1, 2, 3],
        ]  # NOTE bool (False/True) doesn't raise this warning
        for i, val in enumerate(bad_values):
            with self.subTest(i=i):
                with self.assertWarns(FailedEPICSOperationWarning) as w:
                    self.signal.put(val)

                self.assertTrue(str(type(val)) in str(w.warnings[0].message))


class TestStringPV(unittest.TestCase):
    def setUp(self):
        self.name = "TEST-PV-1"
        self.signal = StringPV(name=self.name, protocol="CA", read_only=False)
        self.signal._pv = MagicMock()

    def test_get(self):
        self.signal._pv.get = MagicMock(return_value="test")

        result = self.signal.get()

        self.assertEqual(result, "test")

    def test_get_bad_values(self):
        bad_values = [5, 5.5, [1, 2, 3], True]
        for i, expected_val in enumerate(bad_values):
            with self.subTest(i=i):
                self.signal._pv.get = MagicMock(return_value=expected_val)

                with self.assertWarns(FailedEPICSOperationWarning) as w:
                    self.signal.get()

                self.assertTrue(str(type(expected_val)) in str(w.warnings[0].message))

    def test_put(self):
        val = "test"
        self.signal.put(val)
        self.signal._pv.put.assert_called_once_with(val)

    def test_bad_put(self):
        bad_values = [5, 5.5, [1, 2, 3], True]
        for i, val in enumerate(bad_values):
            with self.subTest(i=i):
                with self.assertWarns(FailedEPICSOperationWarning) as w:
                    self.signal.put(val)

                self.assertTrue(str(type(val)) in str(w.warnings[0].message))


class TestStatePV(unittest.TestCase):
    def setUp(self):
        self.name = "TEST-PV-1"
        self.states = {"NOK": 0, "OK": 1}
        self.signal = StatePV(
            name=self.name, protocol="CA", read_only=False, states=self.states
        )
        self.signal._pv = MagicMock()

    def test_states(self):
        self.assertEqual(self.signal.states.NOK.value, 0)
        self.assertEqual(self.signal.states.OK.value, 1)

    def test_get(self):
        expected_values = [
            (0, self.signal.states.NOK),
            (1, self.signal.states.OK),
            (False, self.signal.states.NOK),
            (True, self.signal.states.OK),
        ]
        for i, (val, expected_state) in enumerate(expected_values):
            with self.subTest(i=i):
                self.signal._pv.get = MagicMock(return_value=val)

                result = self.signal.get()

                self.assertEqual(result, expected_state)

    def test_get_bad_states(self):
        bad_values = [5, 2.0]
        for i, expected_val in enumerate(bad_values):
            with self.subTest(i=i):
                self.signal._pv.get = MagicMock(return_value=expected_val)

                with self.assertWarns(FailedEPICSOperationWarning) as w:
                    self.signal.get()

                self.assertTrue(
                    "Could not find valid state map" in str(w.warnings[0].message)
                )

    def test_get_bad_values(self):
        bad_values = [[1, 2, 3], "test"]
        for i, expected_val in enumerate(bad_values):
            with self.subTest(i=i):
                self.signal._pv.get = MagicMock(return_value=expected_val)

                with self.assertWarns(FailedEPICSOperationWarning) as w:
                    self.signal.get()
                self.assertTrue(str(type(expected_val)) in str(w.warnings[0].message))

    def test_put(self):
        good_values = [(0, 0), (1, 1), ("NOK", 0), ("OK", 1)]
        for i, (val, set_val) in enumerate(good_values):
            self.signal._pv.put.reset_mock()
            with self.subTest(i=i):
                self.signal.put(val)
                self.signal._pv.put.assert_called_once_with(set_val)

    def test_bad_put_states(self):
        bad_values = [2, "BAD", 5.5]  # valid types but not in state map
        for i, val in enumerate(bad_values):
            with self.subTest(i=i):
                with self.assertWarns(FailedEPICSOperationWarning) as w:
                    self.signal.put(val)

                self.assertTrue(
                    "Could not find valid state map" in str(w.warnings[0].message)
                )

    def test_bad_put_types(self):
        bad_values = [[1, 2, 3], True]  # invalid types
        for i, val in enumerate(bad_values):
            with self.subTest(i=i):
                with self.assertWarns(FailedEPICSOperationWarning) as w:
                    self.signal.put(val)

                # NOTE should this be the right warning?
                self.assertTrue(
                    "Could not find valid state map" in str(w.warnings[0].message)
                )


class TestBinaryPV(unittest.TestCase):
    def setUp(self):
        self.name = "TEST-PV-1"
        self.signal = BinaryPV(name=self.name, protocol="CA", read_only=False)
        self.signal._pv = MagicMock()

    def test_get(self):
        expected_values = [
            (0, 0),
            (1, 1),
            (False, 0),
            (True, 1),
            (
                2,
                1,
            ),  # here we convert any integer to a bool - is this correct behaviour?
            (
                100,
                1,
            ),  # here we convert any integer to a bool - is this correct behaviour?
        ]
        for i, (val, expected_state) in enumerate(expected_values):
            with self.subTest(i=i):
                self.signal._pv.get = MagicMock(return_value=val)

                result = self.signal.get()

                self.assertEqual(result, expected_state)

    def test_get_bad_values(self):
        bad_values = [[1, 2, 3], "test", 5.5]
        for i, expected_val in enumerate(bad_values):
            with self.subTest(i=i):
                self.signal._pv.get = MagicMock(return_value=expected_val)

                with self.assertWarns(FailedEPICSOperationWarning) as w:
                    self.signal.get()
                self.assertTrue(str(type(expected_val)) in str(w.warnings[0].message))

    def test_put(self):
        good_values = [(0, 0), (1, 1), (False, 0), (True, 1)]
        for i, (val, set_val) in enumerate(good_values):
            self.signal._pv.put.reset_mock()
            with self.subTest(i=i):
                self.signal.put(val)
                self.signal._pv.put.assert_called_once_with(set_val)

    def test_bad_put_types(self):
        bad_values = [[1, 2, 3], "test", 5, 6.5]
        for i, val in enumerate(bad_values):
            with self.subTest(i=i):
                with self.assertWarns(FailedEPICSOperationWarning) as w:
                    self.signal.put(val)

                self.assertTrue(
                    f"Cannot put value of type {str(type(val))}"
                    in str(w.warnings[0].message)
                )
