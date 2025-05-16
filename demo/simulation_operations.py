import time

from easyssp_simulation.client import SimulationClient
from pydantic import StrictStr


def poll_status_until_finished(simulation_id: StrictStr, simulation_client: SimulationClient) -> str:
    """
    Method for polling the simulation status until it finishes
    :param simulation_id: The simulation id
    :param simulation_client: The simulation client
    :return: The simulation status
    """
    status = ""

    while status not in ["done", "stopped", "time_out", "error"]:
        try:
            time.sleep(5)
        except Exception as ex:
            print(f"An error occurred during sleep {ex}")

        status = simulation_client.get_simulation(simulation_id=simulation_id).data.runs[0].run_status
        print(f"Current Simulation Status: {status}")

    return status


def download_sampled_result(run_id: StrictStr, simulation_client: SimulationClient) -> None:
    """
    Method for downloading sampled results of a simulation run
    :param run_id: The run id
    :param simulation_client: The simulation client
    :return: None
    """
    print("Will download sampled result file ...")
    with open("../output/result_sampled.csv", "wb") as file:
        try:
            intermediate_simulation_results = simulation_client.get_simulation_result_sample(
                run_id=run_id).data
            file.write(intermediate_simulation_results)
        except Exception as ex:
            print(ex)


def download_result(run_id: StrictStr, simulation_client: SimulationClient) -> None:
    """
    Method for downloading results of a simulation run
    :param run_id: The run id
    :param simulation_client: The simulation client
    :return: None
    """
    print("Will download result file ...")
    with open("../output/result.csv", "wb") as file:
        try:
            simulation_results = simulation_client.get_simulation_result(run_id=run_id).data
            file.write(simulation_results)
        except Exception as ex:
            print(ex)


def download_step_log(step_id: StrictStr, step_name: StrictStr, simulation_client: SimulationClient) -> None:
    """
    Method for downloading step log
    :param step_id: The step id
    :param step_name: The step name
    :param simulation_client: The simulation client
    :return: None
    """
    print(f"Will download log for {step_name} step ...")
    with open(f"../output/{step_name}_log.txt", "wb") as file:
        try:
            simulation_log = simulation_client.get_simulation_log(step_id=step_id).data
            file.write(simulation_log)
        except Exception as ex:
            print(ex)


def delete_simulation(simulation_id: StrictStr, simulation_client: SimulationClient) -> None:
    """
    Method for deleting a simulation
    :param simulation_id: The simulation id
    :param simulation_client: The simulation client
    :return: None
    """
    try:
        simulation_client.delete_simulation(simulation_id=simulation_id)
        print(f"Deleted simulation {simulation_id}")
    except Exception as ex:
        print(f"Did not delete simulation {simulation_id}. Cause: {ex}")
