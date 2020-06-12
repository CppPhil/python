from __future__ import absolute_import, division, print_function, unicode_literals

import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf
import tensorflow_probability as tfp

import pandas as pd

# hidden markov models
# there are states (they are hidden, because they're not directly observed)
# observations: Each state has a particular outcome or observation associated with it based on a
#               probability distribution. Example: On a hot day Tim has a 80% chance of being happy
#               and a 20% chance of being sad.
# Transitions:  Each state will have a probability defining the likelihood of transitioning to a
#               different state.

# weather model
# We will model a simple weather system and try to predict the temperature on each day given the following information.
# 1. Cold days are encoded by a 0 and hot days are encoded by a 1.
# 2. The first day in our sequence has an 80% chance of being cold.
# 3. A cold day has a 30% chance of being followed by a hot day.
# 4. A hot day has a 20% chance of being followed by a cold day.
# 5. On each day the temperature is
#  normally distributed with mean and standard deviation 0 and 5 on
#  a cold day and mean and standard deviation 15 and 10 on a hot day.
tfd = tfp.distributions  # making a shortcut for later on
initial_distribution = tfd.Categorical(probs=[0.8, 0.2])  # Refer to point 2 above
transition_distribution = tfd.Categorical(probs=[[0.7, 0.3],
                                                 [0.2, 0.8]])  # refer to points 3 and 4 above
observation_distribution = tfd.Normal(loc=[0., 15.], scale=[5., 10.])  # refer to point 5 above

# the loc argument represents the mean and the scale is the standard deviation

# steps is the amount of days to predict
model = tfd.HiddenMarkovModel(
    initial_distribution=initial_distribution,
    transition_distribution=transition_distribution,
    observation_distribution=observation_distribution,
    num_steps=7)

mean = model.mean()  # Calculate the probabilities

# Session has to be used because model.mean() only creates a partially formed tensor.
# Print the next 7 temperatures for the next 7 days
with tf.compat.v1.Session() as sess:
    print(mean.numpy())
