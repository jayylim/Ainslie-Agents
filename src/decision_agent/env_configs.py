
# Control Block

param_config = {
   # Parameters for each variable type (might be abstracted differently)
    "env_params": {
        "grid":{
            "width": 10,
            "height": 10,
            "start": (1, 2),
            "rewards": {
                "SS": {
                    "position": (4, 5),
                    "value": 5
                },
                "LL": {
                    "position": (8, 1),
                    "value": 10
                }
            }
        }, # continue other model type here if necessary
        "timeline":{
            "length": None, 
            "start": 0,
            "rewards": {
                "SS": {
                    "value": 5,
                    "delay": 6
                },
                "LL": {
                    "value": 15,
                    "delay": 10
                }
            }
        },
         "Rtimeline":{
            "length": None,
            "start": 0,
            "rewards": {
                "SS": {
                    "value": 5,
                    "delay": 6
                },
                "LL": {
                    "value": 15,
                    "delay": 10
                }
            }
         }
    }
}

