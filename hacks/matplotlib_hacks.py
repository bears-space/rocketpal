import logging
from pathlib import Path
import matplotlib.pyplot as plt
import typing as t
import random

SAVEFIG_DPI = 300


def get_matplotlib_supported_file_endings() -> t.List[str]:
    """Gets the file endings supported by matplotlib.

    Returns
    -------
    list[str]
        List of file endings prepended with a dot
    """
    # Get matplotlib's supported file ending and return them (without descriptions, hence only keys)
    filetypes = plt.gcf().canvas.get_supported_filetypes().keys()

    # Ensure the dot is included in the filetype endings
    filetypes = ["." + filetype for filetype in filetypes]

    return filetypes


def hack_override_matplotlib_show(filename: str | None = None) -> None:
    """HACK: Override matplotlib's show function so that it instead saves
    the plot to the filename you define. The intention is to call this function
    before any library method which internally calls matplotlib.show, so that
    that functions saves to that file instead of opening a matplotlib window.

    Parameters
    ----------
    filename : str | None, optional
        The file matplotlib.show plots will be redirected to, by default None
    """
    # If filename is None, generate a random filename
    if filename is None:
        filename = f"output/unnamed/{random.randint(0, 1234567)}.png"

    # Dynamically generate a function that has the same interface as matplotlib.show, but saves the plots to disk instead
    def fake_show_with_redirection_to_disk(*, block=None) -> None:
        # Warn if file ending is not supported
        file_ending = Path(filename).suffix
        if file_ending not in get_matplotlib_supported_file_endings():
            logging.warning(
                f"Unsupported file ending '{file_ending}' for matplotlib show to save redirection!"
            )

        # Before export, ensure the folder the file should go into exists
        Path(filename).parent.mkdir(parents=True, exist_ok=True)

        # Save the plot
        plt.savefig(filename, dpi=SAVEFIG_DPI)
        plt.close()

    # HACK Override matplotlib's show
    plt.show = fake_show_with_redirection_to_disk
