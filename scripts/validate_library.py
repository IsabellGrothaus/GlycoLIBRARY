from pathlib import Path
import sys


LIBRARY = Path("library")


def validate_library():
    errors = []

    if not LIBRARY.exists():
        errors.append("Library directory does not exist.")

    for glycan_dir in LIBRARY.rglob("*"):
        if not glycan_dir.is_dir():
            continue

        # example validation
        if glycan_dir.name.startswith("."):
            continue

        # your actual rules here


    if errors:
        print("Validation failed:")
        for error in errors:
            print(f"  - {error}")

        sys.exit(1)

    print("Glycan library validation successful.")


if __name__ == "__main__":
    validate_library()
