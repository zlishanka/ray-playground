from ray.train import ScalingConfig


def train_func():
    """User-defined training function that runs on each distributed worker process.

    This function typically contains logic for loading the model,
    loading the dataset, training the model, saving checkpoints,
    and logging metrics.
    """
    ...

# The ScalingConfig is the mechanism for defining the scale of the training job
# Specify two basic parameters for worker parallelism and compute resources:

# - num_workers: The number of workers to launch for a distributed training job.
# - use_gpu: Whether each worker should use a GPU or CPU.

# Single worker with a CPU
scaling_config = ScalingConfig(num_workers=1, use_gpu=False)

# Single worker with a CPU
#scaling_config = ScalingConfig(num_workers=1, use_gpu=False)

# Multiple workers, each with a GPU
#scaling_config = ScalingConfig(num_workers=4, use_gpu=True)

# Trainers 
'''
Launching workers as defined by the scaling_config.
Setting up the framework’s distributed environment on all workers.
Running the train_func on all workers.
'''

from ray.train.torch import TorchTrainer

trainer = TorchTrainer(train_func, scaling_config=scaling_config)
trainer.fit()