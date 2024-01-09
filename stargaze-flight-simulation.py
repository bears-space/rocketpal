#!/usr/bin/env python3


from core.flight_simulation import FlightSimulation


def main() -> None:
    # Initialize flight simulation
    sim: FlightSimulation = FlightSimulation()

    # TODO Load flight parameters

    # Show infos about configured flight
    sim.show_input_info()

    # Run simulation
    sim.simulate()

    # Show and save results
    sim.show_results()
    sim.export_results()


# Run main if launched directly
if __name__ == "__main__":  # type: ignore
    main()
