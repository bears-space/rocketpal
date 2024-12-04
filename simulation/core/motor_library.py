import os
import typing as t

from parsers.motor_config import MotorConfig


class MotorLibrary:
    motors: t.Dict[str, MotorConfig]

    def __init__(self, motor_library_folder: str) -> None:
        self.motors = {}

        # Load motors from folder
        files: t.List[str] = os.listdir(motor_library_folder)
        files = [filename for filename in files if filename.find(".yaml") != -1]
        for filename in files:
            with open(motor_library_folder + "/" + filename) as file:
                motor: MotorConfig = MotorConfig(file)
                self.motors[motor.id] = motor

    def get(self, motor_id: str) -> t.Union[MotorConfig, None]:
        """Get the motor config belonging to the given motor_id, or None.

        Args:
            motor_id (str): The id of the motor to get.

        Returns:
            t.Union[MotorConfig, None]: The motor that has the given id, or None if it doesn't exist in the library.
        """
        return self.motors.get(motor_id, None)
