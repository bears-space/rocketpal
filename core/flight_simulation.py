from rocketpy import Environment, Rocket, SolidMotor, Flight
import datetime
from pathlib import Path


class FlightSimulation:
    def __init__(self) -> None:
        # NOTE This is temporary test code based on RocketPy docs, see https://docs.rocketpy.org/en/latest/user/first_simulation.html

        # Setup environment
        env = Environment(
            latitude=int(32.990254), longitude=int(-106.974998), elevation=1400
        )
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)
        env.set_date(
            (tomorrow.year, tomorrow.month, tomorrow.day, 12), timezone="America/Denver"
        )
        env.set_atmospheric_model(type="Forecast", file="GFS")

        # Print environment info
        print("ENVIRONMENT INFO START")
        env.info()
        print("ENVIRONMENT INFO END")

        # Setup motor
        Pro75M1670 = SolidMotor(
            thrust_source="data/motors/Cesaroni_M1670.eng",
            dry_mass=1.815,
            dry_inertia=(0.125, 0.125, 0.002),
            nozzle_radius=33 / 1000,
            grain_number=5,
            grain_density=1815,
            grain_outer_radius=33 / 1000,
            grain_initial_inner_radius=15 / 1000,
            grain_initial_height=120 / 1000,
            grain_separation=5 / 1000,
            grains_center_of_mass_position=0.397,
            center_of_dry_mass_position=0.317,
            nozzle_position=0,
            burn_time=3.9,
            throat_radius=11 / 1000,
            coordinate_system_orientation="nozzle_to_combustion_chamber",
        )

        # Print motor info
        print("MOTOR INFO START")
        Pro75M1670.info()
        print("MOTOR INFO END")

        # Create rocket
        calisto = Rocket(
            radius=127 / 2000,
            mass=14.426,
            inertia=(6.321, 6.321, 0.034),
            power_off_drag="data/calisto/powerOffDragCurve.csv",
            power_on_drag="data/calisto/powerOnDragCurve.csv",
            center_of_mass_without_motor=0,
            coordinate_system_orientation="tail_to_nose",
        )

        # Add motor to rocket
        calisto.add_motor(Pro75M1670, position=-1.255)

        # Add rail guides
        rail_buttons = calisto.set_rail_buttons(
            upper_button_position=0.0818,
            lower_button_position=-0.6182,
            angular_position=45,
        )

        # Add aerodynamic components
        nose_cone = calisto.add_nose(length=0.55829, kind="von karman", position=1.278)
        fin_set = calisto.add_trapezoidal_fins(
            n=4,
            root_chord=0.120,
            tip_chord=0.060,
            span=0.110,
            position=-1.04956,
            cant_angle=int(0.5),
            airfoil=("data/calisto/NACA0012-radians.csv", "radians"),
        )
        tail = calisto.add_tail(
            top_radius=0.0635, bottom_radius=0.0435, length=0.060, position=-1.194656
        )

        # Add parachutes
        main = calisto.add_parachute(
            name="main",
            cd_s=10.0,
            trigger=800,  # ejection altitude in meters
            sampling_rate=105,
            lag=int(1.5),
            noise=(0, 8.3, 0.5),
        )
        drogue = calisto.add_parachute(
            name="drogue",
            cd_s=1.0,
            trigger="apogee",  # ejection at apogee
            sampling_rate=105,
            lag=int(1.5),
            noise=(0, 8.3, 0.5),
        )

        # Show graphics about the rocket
        print("ROCKET GRAPHICS START")
        calisto.plots.static_margin()
        calisto.draw()
        print("ROCKET GRAPHICS END")

        # Run the simulation
        test_flight = Flight(
            rocket=calisto, environment=env, rail_length=5.2, inclination=85, heading=0
        )

        # Print simulation results
        print("RESULTS INFO START")
        test_flight.info()
        print("RESULTS INFO END")

        # Show simulation results graphics
        print("RESULTS GRAPHICS START")
        test_flight.all_info()
        print("RESULTS GRAPHICS END")

        # Before export, ensure output folder exists
        Path("output").mkdir(parents=True, exist_ok=True)

        # Export flight data
        test_flight.export_data("output/calisto_flight_data.csv")

        # Export trajectory for Google Earth visulization
        test_flight.export_kml(
            file_name="output/trajectory.kml",
            extrude=True,
            altitude_mode="relative_to_ground",
        )
