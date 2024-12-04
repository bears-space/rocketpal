import os
import typing as t

from parsers.parachute_config import ParachuteConfig


class ParachuteLibrary:
    parachutes: t.Dict[str, ParachuteConfig]

    def __init__(self, parachute_library_folder: str) -> None:
        self.parachutes = {}

        # Load motors from folder
        files: t.List[str] = os.listdir(parachute_library_folder)
        files = [filename for filename in files if filename.find(".yaml") != -1]
        for filename in files:
            with open(parachute_library_folder + "/" + filename) as file:
                parachute: ParachuteConfig = ParachuteConfig(file)
                self.parachutes[parachute.id] = parachute

    def get(self, parachute_id: str) -> t.Union[ParachuteConfig, None]:
        """Get the parachute config belonging to the given parachute_id, or None.

        Args:
            parachute_id (str): The id of the parachute to get.

        Returns:
            t.Union[ParachuteConfig, None]: The parachute that has the given id, or None if it doesn't exist in the library.
        """
        return self.parachutes.get(parachute_id, None)
