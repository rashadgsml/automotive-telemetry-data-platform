
from telemetry.data_quality import run_quality_checks


def test_quality_checks_pass_for_current_data():
    results = run_quality_checks()

    assert results["total_records"] >= 0
    assert results["missing_values"] == 0
    assert results["invalid_sensor_records"] == 0
    assert results["passed"] is True
