import os
import typing as t

from parsers.location import Location


class LocationLibrary:
    locations: t.Dict[str, Location]

    def __init__(self, location_library_folder: str) -> None:
        self.locations = {}

        # Load locations from folder
        files: t.List[str] = os.listdir(location_library_folder)
        files = [filename for filename in files if filename.find(".yaml") != -1]
        for filename in files:
            with open(location_library_folder + "/" + filename) as file:
                location: Location = Location(file)
                self.locations[location.id] = location

    def get(self, location_id: str) -> t.Union[Location, None]:
        """Get the location belonging to the given location_id, or None.

        Args:
            location_id (str): The id of the location to get.

        Returns:
            t.Union[Location, None]: The location that has the given id, or None if it doesn't exist in the library.
        """
        return self.locations.get(location_id, None)
