start_simulation_json_config = """
    {
        "name": "Python Client Test Simulation",
        "runs": [
        {
          "name": "Python Client Run 1",
          "ssdFileName": "SystemStructure.ssd",
          "maxRunDurationInMinutes": 1,
          "stimuliFileName": "exampleStimuli.csv",
          "hardwareIdentifier": 123,
          "start": 0,
          "step": 0.01,
          "stop": 100,
          "targetType": "Linux64"
        },
        {
          "name": "Python Client Run 2",
          "ssdFileName": "SystemStructure.ssd",
          "maxRunDurationInMinutes": 2,
          "stimuliFileName": "exampleStimuli.csv",
          "hardwareIdentifier": 123,
          "start": 1,
          "step": 0.01,
          "stop": 102,
          "outputRate": 2,
          "targetType": "Linux64"
        }
    ]
}
"""
