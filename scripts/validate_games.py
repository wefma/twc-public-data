import json
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    with (ROOT / "games.yml").open(encoding="utf-8") as games_file:
        games = yaml.safe_load(games_file)
    with (ROOT / "games.schema.json").open(encoding="utf-8") as schema_file:
        schema = json.load(schema_file)

    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = sorted(validator.iter_errors(games), key=lambda error: list(error.absolute_path))
    if errors:
        for error in errors:
            path = ".".join(str(part) for part in error.absolute_path) or "<root>"
            print(f"{path}: {error.message}")
        raise SystemExit(1)

    print("games.yml conforms to games.schema.json")


if __name__ == "__main__":
    main()
