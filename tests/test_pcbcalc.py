from __future__ import annotations

import csv
import tempfile
import unittest
from argparse import Namespace
from pathlib import Path

from scripts import pcbcalc


class ImpedanceTests(unittest.TestCase):
    def test_microstrip_target_round_trip(self) -> None:
        width = pcbcalc.solve_positive(
            lambda value: pcbcalc.microstrip_impedance(value, 0.20, 4.3)["z0_ohm"],
            50.0,
        )
        impedance = pcbcalc.microstrip_impedance(width, 0.20, 4.3)["z0_ohm"]
        self.assertAlmostEqual(impedance, 50.0, places=6)

    def test_stripline_target_round_trip(self) -> None:
        width = pcbcalc.solve_positive(
            lambda value: pcbcalc.stripline_impedance(value, 0.30, 4.3)["z0_ohm"],
            50.0,
        )
        impedance = pcbcalc.stripline_impedance(width, 0.30, 4.3)["z0_ohm"]
        self.assertAlmostEqual(impedance, 50.0, places=6)

    def test_differential_microstrip_is_less_than_twice_single_ended(self) -> None:
        values = pcbcalc.differential_microstrip_ohm(0.18, 0.18, 0.20, 4.3)
        self.assertLess(values["zdiff_ohm"], 2.0 * values["z_single_ohm"])
        self.assertGreater(values["zdiff_ohm"], values["z_single_ohm"])

    def test_differential_microstrip_target_round_trip(self) -> None:
        width = pcbcalc.solve_positive(
            lambda value: pcbcalc.differential_microstrip_ohm(value, 0.18, 0.20, 4.3)["zdiff_ohm"],
            90.0,
        )
        impedance = pcbcalc.differential_microstrip_ohm(width, 0.18, 0.20, 4.3)["zdiff_ohm"]
        self.assertAlmostEqual(impedance, 90.0, places=6)


class PowerTests(unittest.TestCase):
    def test_trace_width_is_positive_and_margin_applies(self) -> None:
        args = Namespace(
            current_a=1.0,
            temp_rise_c=10.0,
            copper_oz=1.0,
            internal=False,
            margin_percent=25.0,
            width_mm=None,
            length_mm=50.0,
            ambient_c=25.0,
            drop_limit_mv=100.0,
        )
        result = pcbcalc.cmd_trace_width(args)
        self.assertGreater(result["required_width_mm"], 0.20)
        self.assertLess(result["required_width_mm"], 0.40)
        self.assertAlmostEqual(
            result["recommended_width_mm"],
            result["required_width_mm"] * 1.25,
        )
        self.assertTrue(result["drop_limit_pass"])

    def test_internal_trace_is_wider_than_external_for_same_current(self) -> None:
        external = pcbcalc.ipc2221_width_mm(1.0, 10.0, 1.0, external=True)
        internal = pcbcalc.ipc2221_width_mm(1.0, 10.0, 1.0, external=False)
        self.assertGreater(internal, external)

    def test_via_current_estimate(self) -> None:
        args = Namespace(
            hole_mm=0.30,
            plating_um=25.0,
            count=1,
            board_mm=1.60,
            temp_rise_c=10.0,
            ambient_c=25.0,
            derating=0.70,
        )
        result = pcbcalc.cmd_via_current(args)
        self.assertGreater(result["single_via_capacity_a"], 0.5)
        self.assertLess(result["single_via_capacity_a"], 1.0)

    def test_ldo_thermal_margin(self) -> None:
        args = Namespace(
            vin=5.0,
            vout=3.3,
            current_a=0.5,
            theta_ja_c_per_w=40.0,
            ambient_c=50.0,
            max_tj_c=125.0,
            dropout_v=1.0,
        )
        result = pcbcalc.cmd_ldo(args)
        self.assertAlmostEqual(result["power_dissipation_w"], 0.85)
        self.assertAlmostEqual(result["junction_temp_c"], 84.0)
        self.assertAlmostEqual(result["temperature_margin_c"], 41.0)
        self.assertTrue(result["thermal_pass"])
        self.assertTrue(result["dropout_pass"])

    def test_battery_life(self) -> None:
        args = Namespace(
            capacity_mah=1000.0,
            average_current_ma=50.0,
            efficiency_percent=100.0,
            usable_percent=80.0,
            derating_percent=90.0,
        )
        result = pcbcalc.cmd_battery_life(args)
        self.assertAlmostEqual(result["runtime_hours"], 14.4)

    def test_buck_inductor(self) -> None:
        args = Namespace(
            vin=5.0,
            vout=3.3,
            fsw_hz=500_000.0,
            iout=1.0,
            ripple_ratio=0.3,
            saturation_margin=1.3,
        )
        result = pcbcalc.cmd_buck_inductor(args)
        self.assertAlmostEqual(result["inductance_uh"], 7.48, places=2)
        self.assertAlmostEqual(result["peak_current_a"], 1.15)
        self.assertAlmostEqual(result["recommended_saturation_current_a"], 1.495)

    def test_rc_filter(self) -> None:
        args = Namespace(resistance_ohm=10_000.0, capacitance_uf=0.1)
        result = pcbcalc.cmd_rc_filter(args)
        self.assertAlmostEqual(result["tau_ms"], 1.0)
        self.assertAlmostEqual(result["cutoff_hz"], 159.154943, places=5)

    def test_voltage_divider(self) -> None:
        args = Namespace(
            vin=5.0,
            r_top_ohm=10_000.0,
            r_bottom_ohm=20_000.0,
            target_vout=None,
        )
        result = pcbcalc.cmd_voltage_divider(args)
        self.assertAlmostEqual(result["vout_v"], 3.3333333333, places=6)


class PowerBudgetTests(unittest.TestCase):
    def test_power_budget_csv(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "budget.csv"
            with path.open("w", newline="", encoding="utf-8") as handle:
                writer = csv.writer(handle)
                writer.writerow(["rail", "component", "voltage_v", "current_ma", "duty_percent"])
                writer.writerow(["3V3", "MCU", "3.3", "100", "50"])
                writer.writerow(["3V3", "Sensor", "3.3", "10", "100"])
            args = Namespace(csv=str(path))
            result = pcbcalc.cmd_power_budget(args)
        self.assertAlmostEqual(result["rail_totals"]["3V3"]["power_mw"], 198.0)
        self.assertAlmostEqual(result["total_average_power_mw"], 198.0)


class ValidationTests(unittest.TestCase):
    def test_invalid_inputs_raise(self) -> None:
        with self.assertRaises(pcbcalc.CalculationError):
            pcbcalc.ipc2221_width_mm(0.0, 10.0, 1.0, external=True)
        with self.assertRaises(pcbcalc.CalculationError):
            pcbcalc.microstrip_impedance(0.2, 0.2, 0.9)
        with self.assertRaises(pcbcalc.CalculationError):
            pcbcalc.solve_positive(lambda value: 1.0, 2.0)


if __name__ == "__main__":
    unittest.main()
