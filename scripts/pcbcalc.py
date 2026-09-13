#!/usr/bin/env python3
"""Deterministic planning calculators for common PCB design checks.

The formulas in this file are deliberately transparent and dependency-free.
They are intended for early sizing and review. Controlled impedance, high
current, and safety-critical designs require the fabricator's stackup, a
field solver, or measured validation.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from pathlib import Path
from typing import Any, Callable, Sequence

MIL_PER_MM = 1000.0 / 25.4
MM_PER_MIL = 25.4 / 1000.0
OZ_TO_UM = 34.798
OZ_TO_MIL = OZ_TO_UM / 25.4
FREE_SPACE_IMPEDANCE_OHM = 376.730313668
COPPER_RHO_20C_OHM_M = 1.724e-8
COPPER_ALPHA_PER_C = 0.00393


class CalculationError(ValueError):
    """Raised for invalid or unsupported calculator inputs."""


def positive(value: float, name: str) -> float:
    if not math.isfinite(value) or value <= 0:
        raise CalculationError(f"{name} must be a positive finite number")
    return value


def non_negative(value: float, name: str) -> float:
    if not math.isfinite(value) or value < 0:
        raise CalculationError(f"{name} must be a non-negative finite number")
    return value


def copper_resistivity(temp_c: float) -> float:
    return COPPER_RHO_20C_OHM_M * (1.0 + COPPER_ALPHA_PER_C * (temp_c - 20.0))


def ipc2221_area_mil2(current_a: float, temp_rise_c: float, external: bool) -> float:
    """Return the conductor cross-section required by the IPC-2221 relation."""
    positive(current_a, "current")
    positive(temp_rise_c, "temperature rise")
    k = 0.048 if external else 0.024
    return (current_a / (k * temp_rise_c**0.44)) ** (1.0 / 0.725)


def ipc2221_width_mm(
    current_a: float,
    temp_rise_c: float,
    copper_oz: float,
    external: bool,
) -> float:
    positive(copper_oz, "copper weight")
    thickness_mil = copper_oz * OZ_TO_MIL
    area_mil2 = ipc2221_area_mil2(current_a, temp_rise_c, external)
    return (area_mil2 / thickness_mil) * MM_PER_MIL


def conductor_resistance_ohm(
    length_mm: float,
    width_mm: float,
    copper_oz: float,
    temp_c: float,
) -> float:
    non_negative(length_mm, "length")
    positive(width_mm, "width")
    positive(copper_oz, "copper weight")
    thickness_m = copper_oz * OZ_TO_UM * 1e-6
    width_m = width_mm * 1e-3
    length_m = length_mm * 1e-3
    area_m2 = width_m * thickness_m
    return copper_resistivity(temp_c) * length_m / area_m2


def microstrip_impedance(width_mm: float, height_mm: float, er: float) -> dict[str, float]:
    positive(width_mm, "width")
    positive(height_mm, "height")
    if er < 1.0:
        raise CalculationError("relative permittivity must be at least 1")
    u = width_mm / height_mm
    f_u = 6.0 + (2.0 * math.pi - 6.0) * math.exp(-((30.666 / u) ** 0.7528))
    e_eff = (er + 1.0) / 2.0 + (er - 1.0) / (2.0 * math.sqrt(1.0 + 12.0 / u))
    z0 = (
        FREE_SPACE_IMPEDANCE_OHM
        / (2.0 * math.pi)
        * math.log(f_u / u + math.sqrt(1.0 + (2.0 / u) ** 2))
        / math.sqrt(e_eff)
    )
    delay_ps_per_mm = 3.33564 * math.sqrt(e_eff)
    return {"z0_ohm": z0, "e_eff": e_eff, "delay_ps_per_mm": delay_ps_per_mm}


def stripline_impedance(width_mm: float, height_mm: float, er: float) -> dict[str, float]:
    positive(width_mm, "width")
    positive(height_mm, "height")
    if er < 1.0:
        raise CalculationError("relative permittivity must be at least 1")
    u = width_mm / height_mm
    if u < 0.35:
        z0 = 60.0 / math.sqrt(er) * math.log(4.0 * height_mm / (0.67 * math.pi * width_mm))
    else:
        z0 = 120.0 * math.pi / (math.sqrt(er) * (u + 1.393 + 0.667 * math.log(u + 1.444)))
    delay_ps_per_mm = 3.33564 * math.sqrt(er)
    return {"z0_ohm": z0, "e_eff": er, "delay_ps_per_mm": delay_ps_per_mm}


def differential_microstrip_ohm(
    width_mm: float,
    spacing_mm: float,
    height_mm: float,
    er: float,
) -> dict[str, float]:
    positive(spacing_mm, "spacing")
    single = microstrip_impedance(width_mm, height_mm, er)
    s_over_h = spacing_mm / height_mm
    if not 0.1 <= s_over_h <= 1.0:
        # The model remains useful as a rough estimate, but warn the caller.
        pass
    z_diff = 2.0 * single["z0_ohm"] * (1.0 - 0.48 * math.exp(-0.96 * s_over_h))
    return {
        "zdiff_ohm": z_diff,
        "z_single_ohm": single["z0_ohm"],
        "e_eff": single["e_eff"],
        "s_over_h": s_over_h,
    }


def solve_positive(
    function: Callable[[float], float],
    target: float,
    low: float = 1e-4,
    high: float = 100.0,
    iterations: int = 100,
) -> float:
    """Solve a monotonic function with bisection over positive inputs."""
    f_low = function(low) - target
    f_high = function(high) - target
    if f_low == 0:
        return low
    if f_high == 0:
        return high
    if f_low * f_high > 0:
        raise CalculationError("target is outside the supported model range")
    for _ in range(iterations):
        mid = (low + high) / 2.0
        f_mid = function(mid) - target
        if abs(f_mid) < 1e-9:
            return mid
        if f_low * f_mid <= 0:
            high = mid
            f_high = f_mid
        else:
            low = mid
            f_low = f_mid
    return (low + high) / 2.0


def cmd_trace_width(args: argparse.Namespace) -> dict[str, Any]:
    current = positive(args.current_a, "current")
    temp_rise = positive(args.temp_rise_c, "temperature rise")
    copper_oz = positive(args.copper_oz, "copper weight")
    external = not args.internal
    min_width = ipc2221_width_mm(current, temp_rise, copper_oz, external)
    margin = non_negative(args.margin_percent, "margin") / 100.0
    recommended_width = min_width * (1.0 + margin)
    selected_width = args.width_mm or recommended_width
    positive(selected_width, "selected width")
    ambient = args.ambient_c
    conductor_temp = ambient + temp_rise
    resistance = conductor_resistance_ohm(args.length_mm, selected_width, copper_oz, conductor_temp)
    drop_v = current * resistance
    power_w = current**2 * resistance
    result: dict[str, Any] = {
        "calculator": "trace-width",
        "model": "IPC-2221-style planning estimate",
        "inputs": {
            "current_a": current,
            "temp_rise_c": temp_rise,
            "copper_oz": copper_oz,
            "external": external,
            "length_mm": args.length_mm,
            "ambient_c": ambient,
            "margin_percent": args.margin_percent,
        },
        "required_width_mm": min_width,
        "required_width_mil": min_width * MIL_PER_MM,
        "recommended_width_mm": recommended_width,
        "recommended_width_mil": recommended_width * MIL_PER_MM,
        "selected_width_mm": selected_width,
        "selected_width_mil": selected_width * MIL_PER_MM,
        "resistance_ohm": resistance,
        "voltage_drop_v": drop_v,
        "voltage_drop_mv": drop_v * 1000.0,
        "power_loss_w": power_w,
        "conductor_temp_c": conductor_temp,
        "drop_limit_mv": args.drop_limit_mv,
        "drop_limit_pass": (
            None if args.drop_limit_mv is None else drop_v * 1000.0 <= args.drop_limit_mv
        ),
        "warnings": [
            "Use the fabricator's current rules, actual copper thickness, and thermal environment.",
            "IPC-2152 or measured data is preferred for high-current, high-temperature, or safety-critical paths.",
        ],
    }
    return result


def cmd_via_current(args: argparse.Namespace) -> dict[str, Any]:
    hole_mm = positive(args.hole_mm, "hole diameter")
    plating_um = positive(args.plating_um, "plating thickness")
    count = int(positive(args.count, "via count"))
    board_mm = positive(args.board_mm, "board thickness")
    temp_rise = positive(args.temp_rise_c, "temperature rise")
    derating = positive(args.derating, "derating factor")
    if derating > 1.0:
        raise CalculationError("derating factor must be between 0 and 1")

    hole_mil = hole_mm * MIL_PER_MM
    plating_mil = plating_um / 25.4
    area_mil2 = math.pi * hole_mil * plating_mil
    single_capacity = 0.024 * temp_rise**0.44 * area_mil2**0.725 * derating
    total_capacity = single_capacity * count

    barrel_length_m = board_mm * 1e-3
    area_m2 = math.pi * (hole_mm * 1e-3) * (plating_um * 1e-6)
    single_resistance = copper_resistivity(args.ambient_c + temp_rise) * barrel_length_m / area_m2
    parallel_resistance = single_resistance / count

    return {
        "calculator": "via-current",
        "model": "IPC-2221-style barrel estimate with user-selected derating",
        "inputs": {
            "hole_mm": hole_mm,
            "plating_um": plating_um,
            "count": count,
            "board_mm": board_mm,
            "temp_rise_c": temp_rise,
            "derating": derating,
        },
        "single_via_capacity_a": single_capacity,
        "total_capacity_a": total_capacity,
        "single_via_resistance_ohm": single_resistance,
        "parallel_resistance_ohm": parallel_resistance,
        "warnings": [
            "Current sharing between vias is not perfectly uniform.",
            "Filled, capped, plugged, and unfilled vias can behave differently.",
            "Use IPC-2152, the fabricator's data, or measurement for critical current paths.",
        ],
    }


def cmd_microstrip(args: argparse.Namespace) -> dict[str, Any]:
    if args.target_ohm is not None:
        target = positive(args.target_ohm, "target impedance")
        width = solve_positive(
            lambda w: microstrip_impedance(w, args.height_mm, args.er)["z0_ohm"],
            target,
        )
    else:
        width = positive(args.width_mm, "width")
    values = microstrip_impedance(width, args.height_mm, args.er)
    return {
        "calculator": "microstrip",
        "model": "Hammerstad-Jensen ideal zero-thickness microstrip estimate",
        "inputs": {
            "height_mm": args.height_mm,
            "er": args.er,
            "target_ohm": args.target_ohm,
        },
        "width_mm": width,
        "width_mil": width * MIL_PER_MM,
        **values,
        "warnings": [
            "Solder mask, copper thickness, finite ground width, and stackup tolerances are not modeled.",
            "Confirm controlled impedance with the fabricator or a field solver.",
        ],
    }


def cmd_stripline(args: argparse.Namespace) -> dict[str, Any]:
    if args.target_ohm is not None:
        target = positive(args.target_ohm, "target impedance")
        width = solve_positive(
            lambda w: stripline_impedance(w, args.height_mm, args.er)["z0_ohm"],
            target,
        )
    else:
        width = positive(args.width_mm, "width")
    values = stripline_impedance(width, args.height_mm, args.er)
    return {
        "calculator": "stripline",
        "model": "Ideal zero-thickness centered stripline estimate",
        "inputs": {
            "height_mm": args.height_mm,
            "er": args.er,
            "target_ohm": args.target_ohm,
        },
        "width_mm": width,
        "width_mil": width * MIL_PER_MM,
        **values,
        "warnings": [
            "Off-center conductors, copper thickness, and asymmetric builds are not modeled.",
            "Confirm controlled impedance with the fabricator or a field solver.",
        ],
    }


def cmd_diff_microstrip(args: argparse.Namespace) -> dict[str, Any]:
    if args.target_ohm is not None:
        target = positive(args.target_ohm, "target impedance")
        width = solve_positive(
            lambda w: differential_microstrip_ohm(w, args.spacing_mm, args.height_mm, args.er)[
                "zdiff_ohm"
            ],
            target,
        )
    else:
        width = positive(args.width_mm, "width")
    values = differential_microstrip_ohm(width, args.spacing_mm, args.height_mm, args.er)
    return {
        "calculator": "diff-microstrip",
        "model": "Edge-coupled microstrip planning approximation",
        "inputs": {
            "spacing_mm": args.spacing_mm,
            "height_mm": args.height_mm,
            "er": args.er,
            "target_ohm": args.target_ohm,
        },
        "width_mm": width,
        "width_mil": width * MIL_PER_MM,
        **values,
        "warnings": [
            "The approximation is most useful for 0.1 <= width/height <= 2 and 0.1 <= spacing/height <= 1.",
            "Use the transceiver reference design and the fabricator's impedance model for release.",
        ],
    }


def cmd_ldo(args: argparse.Namespace) -> dict[str, Any]:
    vin = positive(args.vin, "input voltage")
    vout = positive(args.vout, "output voltage")
    current = positive(args.current_a, "load current")
    theta_ja = positive(args.theta_ja_c_per_w, "theta JA")
    ambient = args.ambient_c
    max_tj = positive(args.max_tj_c, "maximum junction temperature")
    dropout_v = args.dropout_v
    if dropout_v is None:
        dropout_pass = None
    else:
        dropout_pass = (vin - vout) >= dropout_v
    power = (vin - vout) * current
    junction = ambient + power * theta_ja
    margin = max_tj - junction
    return {
        "calculator": "ldo",
        "inputs": {
            "vin_v": vin,
            "vout_v": vout,
            "current_a": current,
            "theta_ja_c_per_w": theta_ja,
            "ambient_c": ambient,
            "max_tj_c": max_tj,
            "dropout_v": dropout_v,
        },
        "power_dissipation_w": power,
        "junction_temp_c": junction,
        "temperature_margin_c": margin,
        "thermal_pass": margin > 0,
        "dropout_pass": dropout_pass,
        "warnings": [
            "Use the datasheet's actual theta JA for the package, copper area, and airflow.",
            "Check thermal shutdown, current limit, and maximum output current at the real ambient.",
        ],
    }


def cmd_battery_life(args: argparse.Namespace) -> dict[str, Any]:
    capacity = positive(args.capacity_mah, "battery capacity")
    average_current = positive(args.average_current_ma, "average current")
    efficiency = positive(args.efficiency_percent, "converter efficiency") / 100.0
    usable = positive(args.usable_percent, "usable capacity") / 100.0
    derating = positive(args.derating_percent, "derating") / 100.0
    if efficiency > 1.0 or usable > 1.0 or derating > 1.0:
        raise CalculationError("efficiency, usable capacity, and derating must be <= 100%")
    runtime_h = capacity * usable * derating * efficiency / average_current
    return {
        "calculator": "battery-life",
        "inputs": {
            "capacity_mah": capacity,
            "average_current_ma": average_current,
            "efficiency_percent": args.efficiency_percent,
            "usable_percent": args.usable_percent,
            "derating_percent": args.derating_percent,
        },
        "runtime_hours": runtime_h,
        "runtime_days": runtime_h / 24.0,
        "warnings": [
            "Average current must include sleep, radio, sensor, regulator, and self-discharge behavior.",
            "Battery cutoff, temperature, and aging can reduce usable capacity further.",
        ],
    }


def cmd_buck_inductor(args: argparse.Namespace) -> dict[str, Any]:
    vin = positive(args.vin, "input voltage")
    vout = positive(args.vout, "output voltage")
    fsw_hz = positive(args.fsw_hz, "switching frequency")
    iout = positive(args.iout, "output current")
    ripple_ratio = positive(args.ripple_ratio, "ripple ratio")
    if vout >= vin:
        raise CalculationError("buck converter requires vout < vin")
    delta_i = ripple_ratio * iout
    inductance_h = vout * (vin - vout) / (vin * fsw_hz * delta_i)
    peak = iout + delta_i / 2.0
    rms = math.sqrt(iout**2 + delta_i**2 / 12.0)
    duty = vout / vin
    return {
        "calculator": "buck-inductor",
        "inputs": {
            "vin_v": vin,
            "vout_v": vout,
            "fsw_hz": fsw_hz,
            "iout_a": iout,
            "ripple_ratio": ripple_ratio,
        },
        "duty_cycle_ideal": duty,
        "delta_i_a": delta_i,
        "inductance_uh": inductance_h * 1e6,
        "peak_current_a": peak,
        "rms_current_a": rms,
        "recommended_saturation_current_a": peak * args.saturation_margin,
        "warnings": [
            "Ideal duty cycle ignores switch, diode, inductor, and PCB losses.",
            "Check the inductor's saturation, RMS, DCR, temperature rise, and shielding.",
        ],
    }


def cmd_rc_filter(args: argparse.Namespace) -> dict[str, Any]:
    resistance = positive(args.resistance_ohm, "resistance")
    capacitance = positive(args.capacitance_uf, "capacitance") * 1e-6
    tau = resistance * capacitance
    cutoff = 1.0 / (2.0 * math.pi * tau)
    return {
        "calculator": "rc-filter",
        "inputs": {
            "resistance_ohm": resistance,
            "capacitance_uf": args.capacitance_uf,
        },
        "tau_s": tau,
        "tau_ms": tau * 1000.0,
        "cutoff_hz": cutoff,
        "warnings": [
            "This is an ideal first-order RC response.",
            "Source impedance, load impedance, tolerance, leakage, and dielectric behavior change the result.",
        ],
    }


def cmd_voltage_divider(args: argparse.Namespace) -> dict[str, Any]:
    vin = positive(args.vin, "input voltage")
    if args.r_top_ohm and args.r_bottom_ohm:
        r_top = positive(args.r_top_ohm, "top resistance")
        r_bottom = positive(args.r_bottom_ohm, "bottom resistance")
    elif args.r_top_ohm and args.target_vout:
        r_top = positive(args.r_top_ohm, "top resistance")
        target = positive(args.target_vout, "target output")
        if target >= vin:
            raise CalculationError("target output must be less than input voltage")
        r_bottom = r_top * target / (vin - target)
    elif args.r_bottom_ohm and args.target_vout:
        r_bottom = positive(args.r_bottom_ohm, "bottom resistance")
        target = positive(args.target_vout, "target output")
        if target >= vin:
            raise CalculationError("target output must be less than input voltage")
        r_top = r_bottom * (vin - target) / target
    else:
        raise CalculationError("provide both resistor values, or one resistor plus --target-vout")
    vout = vin * r_bottom / (r_top + r_bottom)
    current = vin / (r_top + r_bottom)
    return {
        "calculator": "voltage-divider",
        "inputs": {
            "vin_v": vin,
            "r_top_ohm": r_top,
            "r_bottom_ohm": r_bottom,
            "target_vout_v": args.target_vout,
        },
        "vout_v": vout,
        "divider_current_a": current,
        "divider_current_ma": current * 1000.0,
        "total_power_w": vin * current,
        "warnings": [
            "The load must be negligible compared with the divider current, or include it in the calculation.",
            "Check resistor voltage rating, tolerance, temperature coefficient, and ADC input impedance.",
        ],
    }


def _find_column(fieldnames: Sequence[str], candidates: tuple[str, ...]) -> str | None:
    normalized = {name.strip().lower().replace(" ", "_"): name for name in fieldnames}
    for candidate in candidates:
        key = candidate.lower().replace(" ", "_")
        if key in normalized:
            return normalized[key]
    return None


def cmd_power_budget(args: argparse.Namespace) -> dict[str, Any]:
    path = Path(args.csv)
    if not path.exists():
        raise CalculationError(f"power-budget CSV not found: {path}")
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames:
            raise CalculationError("power-budget CSV has no header row")
        rail_col = _find_column(reader.fieldnames, ("rail", "supply", "voltage_rail"))
        voltage_col = _find_column(reader.fieldnames, ("voltage_v", "voltage", "v"))
        current_col = _find_column(
            reader.fieldnames, ("current_ma", "current", "current_a", "i_ma")
        )
        duty_col = _find_column(reader.fieldnames, ("duty", "duty_cycle", "duty_percent"))
        if not voltage_col or not current_col:
            raise CalculationError("CSV needs voltage and current columns")
        rows: list[dict[str, Any]] = []
        rail_totals: dict[str, dict[str, float]] = {}
        for index, raw in enumerate(reader, start=2):
            try:
                voltage = float(raw[voltage_col])
                current = float(raw[current_col])
                duty = float(raw[duty_col]) if duty_col and raw.get(duty_col) else 100.0
                if duty > 1.0:
                    duty /= 100.0
                if voltage < 0 or current < 0 or not 0 <= duty <= 1:
                    raise ValueError
            except (TypeError, ValueError) as exc:
                raise CalculationError(f"invalid numeric value on CSV row {index}") from exc
            power = voltage * current * duty
            rail = raw.get(rail_col, "unassigned") if rail_col else "unassigned"
            row = {
                "row": index,
                "rail": rail,
                "voltage_v": voltage,
                "current_ma": current,
                "duty": duty,
                "average_power_mw": power,
            }
            rows.append(row)
            total = rail_totals.setdefault(rail, {"current_ma": 0.0, "power_mw": 0.0})
            total["current_ma"] += current * duty
            total["power_mw"] += power
    return {
        "calculator": "power-budget",
        "inputs": {"csv": str(path)},
        "rows": rows,
        "rail_totals": rail_totals,
        "total_average_power_mw": sum(item["power_mw"] for item in rail_totals.values()),
        "warnings": [
            "Duty-cycle current is an average estimate; verify peak currents separately.",
            "Include regulator quiescent current, conversion loss, inrush, and transient loads.",
        ],
    }


def emit(result: dict[str, Any], as_json: bool) -> None:
    if as_json:
        print(json.dumps(result, indent=2, sort_keys=True))
        return
    calculator = result.get("calculator", "calculation")
    print(f"{calculator}:")
    for key, value in result.items():
        if key == "calculator":
            continue
        if isinstance(value, float):
            print(f"  {key}: {value:.6g}")
        elif isinstance(value, (dict, list)):
            print(f"  {key}:")
            print(json.dumps(value, indent=4, sort_keys=True))
        else:
            print(f"  {key}: {value}")


def build_parser() -> argparse.ArgumentParser:
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--json", action="store_true", help="emit machine-readable JSON")

    parser = argparse.ArgumentParser(
        description="PCB planning calculators. Results are estimates, not sign-off.",
        parents=[common],
    )
    sub = parser.add_subparsers(dest="command", required=True)

    trace = sub.add_parser("trace-width", parents=[common], help="estimate trace width")
    trace.add_argument("--current-a", type=float, required=True)
    trace.add_argument("--temp-rise-c", type=float, default=10.0)
    trace.add_argument("--copper-oz", type=float, default=1.0)
    trace.add_argument("--internal", action="store_true", help="use the internal-layer relation")
    trace.add_argument("--length-mm", type=float, default=50.0)
    trace.add_argument("--ambient-c", type=float, default=25.0)
    trace.add_argument("--margin-percent", type=float, default=25.0)
    trace.add_argument(
        "--width-mm", type=float, help="check a selected width instead of the recommendation"
    )
    trace.add_argument("--drop-limit-mv", type=float)
    trace.set_defaults(func=cmd_trace_width)

    via = sub.add_parser("via-current", parents=[common], help="estimate via barrel current")
    via.add_argument("--hole-mm", type=float, default=0.30)
    via.add_argument("--plating-um", type=float, default=25.0)
    via.add_argument("--count", type=int, default=1)
    via.add_argument("--board-mm", type=float, default=1.60)
    via.add_argument("--temp-rise-c", type=float, default=10.0)
    via.add_argument("--ambient-c", type=float, default=25.0)
    via.add_argument("--derating", type=float, default=0.70)
    via.set_defaults(func=cmd_via_current)

    micro = sub.add_parser("microstrip", parents=[common], help="estimate microstrip impedance")
    micro.add_argument("--width-mm", type=float)
    micro.add_argument("--height-mm", type=float, required=True)
    micro.add_argument("--er", type=float, required=True)
    micro.add_argument("--target-ohm", type=float, help="solve width for this impedance")
    micro.set_defaults(func=cmd_microstrip)

    strip = sub.add_parser("stripline", parents=[common], help="estimate stripline impedance")
    strip.add_argument("--width-mm", type=float)
    strip.add_argument("--height-mm", type=float, required=True)
    strip.add_argument("--er", type=float, required=True)
    strip.add_argument("--target-ohm", type=float, help="solve width for this impedance")
    strip.set_defaults(func=cmd_stripline)

    diff = sub.add_parser(
        "diff-microstrip", parents=[common], help="estimate differential microstrip impedance"
    )
    diff.add_argument("--width-mm", type=float)
    diff.add_argument("--spacing-mm", type=float, required=True)
    diff.add_argument("--height-mm", type=float, required=True)
    diff.add_argument("--er", type=float, required=True)
    diff.add_argument("--target-ohm", type=float, help="solve width for this impedance")
    diff.set_defaults(func=cmd_diff_microstrip)

    ldo = sub.add_parser("ldo", parents=[common], help="check LDO thermal margin")
    ldo.add_argument("--vin", type=float, required=True)
    ldo.add_argument("--vout", type=float, required=True)
    ldo.add_argument("--current-a", type=float, required=True)
    ldo.add_argument("--theta-ja-c-per-w", type=float, required=True)
    ldo.add_argument("--ambient-c", type=float, default=25.0)
    ldo.add_argument("--max-tj-c", type=float, default=125.0)
    ldo.add_argument("--dropout-v", type=float)
    ldo.set_defaults(func=cmd_ldo)

    battery = sub.add_parser("battery-life", parents=[common], help="estimate battery runtime")
    battery.add_argument("--capacity-mah", type=float, required=True)
    battery.add_argument("--average-current-ma", type=float, required=True)
    battery.add_argument("--efficiency-percent", type=float, default=100.0)
    battery.add_argument("--usable-percent", type=float, default=100.0)
    battery.add_argument("--derating-percent", type=float, default=100.0)
    battery.set_defaults(func=cmd_battery_life)

    buck = sub.add_parser("buck-inductor", parents=[common], help="select buck inductor")
    buck.add_argument("--vin", type=float, required=True)
    buck.add_argument("--vout", type=float, required=True)
    buck.add_argument("--fsw-hz", type=float, required=True)
    buck.add_argument("--iout", type=float, required=True)
    buck.add_argument("--ripple-ratio", type=float, default=0.30)
    buck.add_argument("--saturation-margin", type=float, default=1.30)
    buck.set_defaults(func=cmd_buck_inductor)

    rc = sub.add_parser("rc-filter", parents=[common], help="calculate an RC time constant")
    rc.add_argument("--resistance-ohm", type=float, required=True)
    rc.add_argument("--capacitance-uf", type=float, required=True)
    rc.set_defaults(func=cmd_rc_filter)

    div = sub.add_parser("voltage-divider", parents=[common], help="calculate a resistor divider")
    div.add_argument("--vin", type=float, required=True)
    div.add_argument("--r-top-ohm", type=float)
    div.add_argument("--r-bottom-ohm", type=float)
    div.add_argument("--target-vout", type=float)
    div.set_defaults(func=cmd_voltage_divider)

    budget = sub.add_parser("power-budget", parents=[common], help="aggregate a CSV power budget")
    budget.add_argument("--csv", required=True)
    budget.set_defaults(func=cmd_power_budget)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        result = args.func(args)
    except CalculationError as exc:
        if getattr(args, "json", False):
            print(json.dumps({"error": str(exc)}, indent=2))
        else:
            print(f"error: {exc}", file=sys.stderr)
        return 2
    emit(result, getattr(args, "json", False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
