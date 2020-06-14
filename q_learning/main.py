import gym  # OpenAI Gym
import matplotlib.pyplot as plt
import numpy as np

env = gym.make('FrozenLake-v0')  # We are going to use the FrozenLake environment
STATES = env.observation_space.n
ACTIONS = env.action_space.n

Q = np.zeros((STATES, ACTIONS))  # Create a matrix with all 0 values.

EPISODES = 1500  # How many times to run the environment from the beginning
MAX_STEPS = 100  # Max number of steps allowed for each run of environment, have a maximum, prevents infinite recursion

LEARNING_RATE = 0.81  # Learning rate, the higher it is the faster the agent learns.
GAMMA = 0.96

RENDER = False  # If you want to see training set to true

epsilon = 0.9  # Start with a 90% chance of picking a random action

rewards = []
for episode in range(EPISODES):

    state = env.reset()  # Reset to the default state
    for _ in range(MAX_STEPS):  # Explore up to MAX_STEPS
        if RENDER:
            env.render()

        # Take an action for every time step.
        if np.random.uniform(0, 1) < epsilon:
            action = env.action_space.sample()
        else:
            action = np.argmax(Q[state, :])

        # Perform the action.
        # _ is the info value.
        next_state, reward, done, _ = env.step(action)

        Q[state, action] \
            = Q[state, action] + LEARNING_RATE * (reward + GAMMA * np.max(Q[next_state, :]) - Q[state, action])

        state = next_state

        if done:  # If it's done (no more progress is possible), then we're done.
            rewards.append(reward)
            epsilon -= 0.001  # Decrease epsilon slightly so that we decrease the chance for a random action
            break  # Reached goal

print(Q)
print(f"Average reward: {sum(rewards) / len(rewards)}:")


# And now we can see our Q values!

# We can plot the training progress and see how the agent improved

def get_average(values):
    return sum(values) / len(values)


avg_rewards = []
for i in range(0, len(rewards), 100):
    avg_rewards.append(get_average(rewards[i: i + 100]))

plt.plot(avg_rewards)
plt.ylabel('average reward')
plt.xlabel('episodes (100\'s)')
plt.show()
