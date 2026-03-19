import csv
from pathlib import Path

import click


@click.command
@click.argument(
    "input_file",
    type=click.Path(exists=True, file_okay=True, dir_okay=False, path_type=Path),
)
@click.argument(
    "output_file",
    type=click.Path(exists=False, file_okay=True, dir_okay=False, path_type=Path),
)
def fix_and_filter_ras_aero_2_csv(input_file: Path, output_file: Path):
    with input_file.open("r") as original:
        reader = csv.reader(original, dialect="excel")
        with output_file.open("w") as fixed:
            writer = csv.writer(fixed, dialect="excel")

            for i, row in enumerate(reader):
                if i == 0:
                    # NOTE: Skip the header (the output shall not have one)
                    continue

                # Only output
                mach = f"{row[0]}.{row[1]}"
                cd = f"{row[3]}.{row[4]}"
                writer.writerow([mach, cd])


if __name__ == "__main__":
    fix_and_filter_ras_aero_2_csv()
