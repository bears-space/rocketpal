from datetime import datetime
import typing as t

import yaml


class Config:
    # Identifier
    id: str

    # Input ids
    location_id: str
    motor_ids: list[str]
    drag_curve_power_on_file: str
    drag_curve_power_off_file: str
    parachute_ids: list[str]
    airbrake_ids: list[str]

    # Simulation settings
    date_difference_days: int
    launch_rail_length: float
    inclination: float
    heading: float
    launch_date: datetime

    # Rocket settings
    diameter: float

    # Export options - Environment
    export_text_environment: bool
    export_plot_environment: bool

    # Export options - Motor
    export_text_motor: bool
    export_plot_thrust: bool

    # Export options - Rocket
    export_plot_static_margin: bool
    export_plot_rocket: bool

    # Export options - Simulation
    export_text_simulation: bool
    export_plot_trajectory_3d: bool
    export_plot_linear_kinematic_data: bool
    export_plot_flight_path_angle_data: bool
    export_plot_attitude_data: bool
    export_plot_angular_kinematics_data: bool
    export_plot_aerodynamic_forces: bool
    export_plot_rail_buttons_forces: bool
    export_plot_energy_data: bool
    export_plot_fluid_mechanics_data: bool
    export_plot_stability_and_control_data: bool
    export_plot_pressure_rocket_altitude: bool
    export_plot_pressure_signals: bool

    # Export options - Analysis
    export_raw_flight_data: bool
    export_flight_data: bool
    export_flight_data_time_step_seconds: float
    export_trajectory_for_google_earth: bool

    def __init__(self, config_file: t.TextIO) -> None:
        # Load yaml file
        data = yaml.safe_load(config_file)

        # Parse identifier
        self.id = str(data["ID"])

        # Parse input ids
        self.location_id = str(data["location"])
        self.motor_ids = data["motors"]
        self.drag_curve_power_on_file = str(data["dragCurvePowerOnFile"])
        self.drag_curve_power_off_file = str(data["dragCurvePowerOffFile"])
        self.parachute_ids = data["parachutes"]
        self.airbrake_ids = data["airbrakes"]

        # Parse simulation settings
        self.date_difference_days = int(data["dateDiff"])
        self.launch_rail_length = float(data["railL"])
        self.inclination = float(data["inclination"])
        self.heading = float(data["heading"])
        self.launch_date = datetime.strptime(
            str(data["launch_date"]), "%Y-%m-%d_%H-%M-%S"
        )

        # Parse rocket settings
        self.diameter = float(data["diameter"])

        # Parse export options - Environment
        self.export_text_environment = bool(data["exportTextEnvironment"])
        self.export_plot_environment = bool(data["exportPlotEnvironment"])

        # Parse export options - Motor
        self.export_text_motor = bool(data["exportTextMotor"])
        self.export_plot_thrust = bool(data["exportPlotThrust"])

        # Parse export options - Rocket
        self.export_plot_static_margin = bool(data["exportPlotStaticMargin"])
        self.export_plot_rocket = bool(data["exportPlotRocket"])

        # Parse export options - Simulation
        self.export_text_simulation = bool(data["exportTextSimulation"])
        self.export_plot_trajectory_3d = bool(data["exportPlotTrajectory3D"])
        self.export_plot_linear_kinematic_data = bool(
            data["exportPlotLinearKinematicData"]
        )
        self.export_plot_flight_path_angle_data = bool(
            data["exportPlotFlightPathAngleData"]
        )
        self.export_plot_attitude_data = bool(data["exportPlotAttitudeData"])
        self.export_plot_angular_kinematics_data = bool(
            data["exportPlotAngularKinematicsData"]
        )
        self.export_plot_aerodynamic_forces = bool(data["exportPlotAerodynamicForces"])
        self.export_plot_rail_buttons_forces = bool(data["exportPlotRailButtonsForces"])
        self.export_plot_energy_data = bool(data["exportPlotEnergyData"])
        self.export_plot_fluid_mechanics_data = bool(
            data["exportPlotFluidMechanicsData"]
        )
        self.export_plot_stability_and_control_data = bool(
            data["exportPlotStabilityAndControlData"]
        )
        self.export_plot_pressure_rocket_altitude = bool(
            data["exportPlotPressureRocketAltitude"]
        )
        self.export_plot_pressure_signals = bool(data["exportPlotPressureSignals"])

        # Parse export options - Analysis
        self.export_raw_flight_data = bool(data["exportRawFlightData"])
        self.export_flight_data = bool(data["exportFlightData"])
        self.export_flight_data_time_step_seconds = float(
            data["exportFlightDataTimeStepSeconds"]
        )
        self.export_trajectory_for_google_earth = bool(
            data["exportTrajectoryForGoogleEarth"]
        )
