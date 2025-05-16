from easyssp_auth import AuthError
from easyssp_simulation.client import SimulationClient
from easyssp_simulation.models import StartSimulationConfiguration
from easyssp_utils.client import ApiException
from pydantic import ValidationError
from simulation_operations import (
    download_result,
    download_sampled_result,
    download_step_log,
    poll_status_until_finished,
)
from start_simulation_config_json import start_simulation_json_config

USER_AGENT = "easyssp-simulation-examples-python"

with (
    open("../input/simulation_example.ssp", "rb") as ssp_file,
    open("../input/exampleStimuli.csv", "rb") as stimuli_file
):
    try:
        simulation_client = SimulationClient(username="your_easyssp_username", password="your_easyssp_password",
                                             user_agent=USER_AGENT)

        # get simulation info and create start configuration
        simulation_info = simulation_client.get_simulation_info().data
        start_simulation_config = StartSimulationConfiguration.from_json(start_simulation_json_config)

        # set the correct hardware identifier in the start configuration
        for run in start_simulation_config.runs:  # type: ignore[union-attr]
            run.hardware_identifier = simulation_info.available_hardware[0].identifier

        # start simulation
        simulation_started = simulation_client.start_simulation(
            configuration=start_simulation_config,  # type: ignore[arg-type]
            ssp_file=ssp_file.read(),
            stimuli_file=[
                ("exampleStimuli.csv",
                 stimuli_file.read())
            ]
        ).data
        simulation_id = simulation_started.simulation.id
        print(f"Simulation Id: {simulation_id}")

        # choose the first simulation run id
        run_id = simulation_started.simulation.runs[0].id
        print(f"Simulation Run Id: {run_id}")
        print(f"Simulation Cost: {simulation_started.total_credit_cost}")

        poll_status_until_finished(simulation_id, simulation_client)  # wait for the simulation to finish
        download_sampled_result(run_id, simulation_client)  # download sampled results
        download_result(run_id, simulation_client)  # download results

        for step in simulation_started.simulation.runs[0].steps:
            download_step_log(step.id, step.step_key, simulation_client)  # download step log
    # catch ValidationError for incorrect request parameters
    # catch ApiException for errors from the API client or the server
    except (AuthError, ApiException, ValidationError) as ex:
        print(ex)
