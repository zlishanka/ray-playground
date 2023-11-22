from ray import train, tune 

# Define an objective function
def objective(config):
    score = config["a"] ** 2 + config["b"]
    return {"score" : score}

# Define a search space
search_space = {
    "a" : tune.grid_search([0.001, 0.01, 0.1, 1.0]),
    "b" : tune.choice([1,2,3]),
}

# Start a tune run and print best result 
tuner = tune.Tuner(objective, param_space=search_space)

results = tuner.fit()
print(results.get_best_result(metric="score", mode="min").config)

# With Tune you can also launch a multi-node distributed hyperparameter sweep 
# in less than 10 lines of code.