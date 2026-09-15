from pathlib import Path

from src.validator import ValidationError, validate_files

ROOT = Path(__file__).resolve().parents[1]

if __name__ == "__main__":
    try:
        messages = validate_files(
            ROOT / "config" / "network_plan.json",
            ROOT / "config" / "firewall_policy.json",
        )
    except ValidationError as exc:
        raise SystemExit(f"VALIDATION FAILED: {exc}") from exc

    print("Architecture validation passed")
    for message in messages:
        print(message)
