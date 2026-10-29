from pathlib import Path
import sys


LIBRARY = Path("library")

REQUIRED_FILES = [
    "angles.dat",
    "colvar.dat",
    "omega_angles.dat",
]


def read_angle_names(file_path):
    """
    Read all angle names from angles.dat or omega_angles.dat.

    Example:
    phi1_2 psi1_2 phi2_3 psi2_3 omega3_4
    """
    names = []

    with open(file_path, "r") as file:
        for line in file:
            # Ignore comments
            line = line.split("#")[0].strip()

            if not line:
                continue

            names.extend(line.split())

    return names


def get_pipeline_directories():
    """
    Find all lowest-level directories underneath library/.

    Examples:
        library/N-glycans/M5/
        library/N-glycans/complex/A2G2S2/
        library/N-glycans/hybrid/...
        library/O-glycans/Core1/

    Intermediate directories such as:
        N-glycans/
        O-glycans/
        complex/
        hybrid/

    are not treated as pipelines.
    """
    pipeline_dirs = []

    for directory in LIBRARY.rglob("*"):
        if not directory.is_dir():
            continue

        subdirectories = [
            child
            for child in directory.iterdir()
            if child.is_dir() and not child.name.startswith(".")
        ]

        if not subdirectories:
            pipeline_dirs.append(directory)

    return pipeline_dirs


def validate_library():
    errors = []

    if not LIBRARY.exists():
        print(f"ERROR: Library directory '{LIBRARY}' does not exist.")
        sys.exit(1)

    pipeline_dirs = get_pipeline_directories()

    if not pipeline_dirs:
        errors.append(
            "No pipeline directories found underneath library/."
        )

    for pipeline_dir in pipeline_dirs:

        print(f"Checking: {pipeline_dir}")

        # -----------------------------------------------------
        # 1. Check required files
        # -----------------------------------------------------

        for required_file in REQUIRED_FILES:
            file_path = pipeline_dir / required_file

            if not file_path.is_file():
                errors.append(
                    f"{pipeline_dir}: missing '{required_file}'"
                )

        # -----------------------------------------------------
        # 2. Read angles.dat and omega_angles.dat
        #    and check corresponding FES files
        # -----------------------------------------------------

        angle_files = [
            pipeline_dir / "angles.dat",
            pipeline_dir / "omega_angles.dat",
        ]

        for angle_file in angle_files:

            # Missing file is already reported above
            if not angle_file.is_file():
                continue

            angle_names = read_angle_names(angle_file)

            for angle_name in angle_names:

                expected_fes_file = (
                    pipeline_dir / f"fes_{angle_name}.dat"
                )

                if not expected_fes_file.is_file():
                    errors.append(
                        f"{pipeline_dir}: "
                        f"'{angle_file.name}' contains '{angle_name}', "
                        f"but '{expected_fes_file.name}' is missing "
                        f"from this pipeline"
                    )

    # ---------------------------------------------------------
    # Report result
    # ---------------------------------------------------------

    if errors:
        print("\nValidation failed:\n")

        for error in errors:
            print(f"  - {error}")

        print(
            f"\nFound {len(errors)} validation error(s)."
        )

        sys.exit(1)

    print("\nGlycan library validation successful.")
    print(
        f"Checked {len(pipeline_dirs)} pipeline directories."
    )

    sys.exit(0)


if __name__ == "__main__":
    validate_library()
