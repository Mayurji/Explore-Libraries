### MLflow tracking provides three main functionalities:

Runs 
    - Execution of code (ml code) is treated as runs \
    - It Records 

        Metadata information (metrics, parameters, start and end times)
        Artifacts (output files -  model weights, images, etc)

Models
    - Logged models contains their own metadata and artifacts

Experiments
    - Group of runs and models for a specific task.

You can use UI, CLI, or APIs to create experiments.

### Tracking Runs

 Functions

- mlflow.start_run()
- mlflow.log_param()
- mlflow.log_metric()
- mlflow.autolog() #before training code

You can log either locally as files, in databases, or remote machine (cloud)

### MLflow 3
        
- powerful search capabilities through mlflow.search_logged_models().
- Search based performance metrics, parameters, or model attributes.
- Enhanced Model Tracking capabilities.
- Allows logging multiple model checkpoints with single run and track
their performance against different datasets.
- Usually helpful while training deep learning models for checkpointing.
- Linking metrics to models and datasets
- You can search and rank model checkpoints based on their performance metrics.
- New model URI format that uses model IDs instead of run IDs.
- Tracking datasets: 
    
    mlflow.log_input()

### Common Setup for MLFlow

- localhost with local file
- localhost with various data stores
- remote tracking with tracking server (cloud storage, databases, etc)