# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: -all
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.16.4
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %% [markdown]
# # Standard Q-learning - allocentric environment

# %% [markdown]
# ## Initialization

# %%
# Import packages
import numpy as np
import pandas as pd

# %%
# Load custom functions
import plotting
from agent import EpsilonGreedy, Qlearning
from environment import CONTEXTS_LABELS, Actions, Cues, WrappedEnvironment
from tqdm import tqdm
from utils import Params

# %%
# Formatting & autoreload stuff
# %load_ext lab_black
# %load_ext autoreload
# %autoreload 2

# %% [markdown]
# ## Choose the task parameters

# %%
# Choose the parameters for the task
params = Params(epsilon=0.1, n_runs=100, numEpisodes=300)
params

# %% [markdown]
# ## Load the environment and the agent algorithms

# %%
# Load the environment
env = WrappedEnvironment(params)

# %%
# Load the agent algorithms
learner = Qlearning(
    learning_rate=params.alpha,
    gamma=params.gamma,
    state_size=env.numStates,
    action_size=env.numActions,
)
explorer = EpsilonGreedy(epsilon=params.epsilon)

# %% [markdown]
# ## States and actions meaning

# %%
# State space
for idx, cue in enumerate(CONTEXTS_LABELS):
    plotting.plot_tiles_locations(
        np.array(list(env.tiles_locations)) + idx * len(env.tiles_locations),
        env.rows,
        env.cols,
        title=CONTEXTS_LABELS[cue],
    )

# %% [markdown]
# ### Correspondance between flat states and (internal) composite states

# %%
state = 63
env.convert_flat_state_to_composite(state)

# %%
env.convert_composite_to_flat_state({"location": 13, "cue": Cues.OdorA})

# %% [markdown]
# ### Action meaning

# %%
action = 0
Actions(action)

# %% [markdown]
# ## Main loop

# %%
rewards = np.zeros((params.numEpisodes, params.n_runs))
steps = np.zeros((params.numEpisodes, params.n_runs))
episodes = np.arange(params.numEpisodes)
qtables = np.zeros((params.n_runs, env.numStates, env.numActions))
all_states = []
all_actions = []

for run in range(params.n_runs):  # Run several times to account for stochasticity
    learner.reset_qtable()  # Reset the Q-table between runs

    for episode in tqdm(
        episodes, desc=f"Run {run+1}/{params.n_runs} - Episodes", leave=False
    ):
        state = env.reset()  # Reset the environment
        step_count = 0
        done = False
        total_rewards = 0

        while not done:
            action = explorer.choose_action(
                action_space=env.action_space(), state=state, qtable=learner.qtable
            )

            # Record states and actions
            all_states.append(state)
            all_actions.append(Actions(action).name)

            # Take the action (a) and observe the outcome state(s') and reward (r)
            new_state, reward, done = env.step(action, state)

            learner.qtable[state, action] = learner.update(
                state, action, reward, new_state
            )

            total_rewards += reward
            step_count += 1

            # Our new state is state
            state = new_state

        # explorer.epsilon = explorer.update_epsilon(episode)

        rewards[episode, run] = total_rewards
        steps[episode, run] = step_count
    qtables[run, :, :] = learner.qtable

# %% [markdown]
# ## Postprocessing

# %%
res = pd.DataFrame(
    data={
        "Episodes": np.tile(episodes, reps=params.n_runs),
        "Rewards": rewards.flatten(order="F"),
        "Steps": steps.flatten(order="F"),
    }
)
res["cum_rewards"] = rewards.cumsum(axis=0).flatten(order="F")
# st = pd.DataFrame(data={"Episodes": episodes, "Steps": steps.mean(axis=1)})
qtable = qtables.mean(axis=0)  # Average the Q-table between runs

# %%
res

# %%
tmp = []
for idx, st in enumerate(tqdm(all_states)):
    tmp.append(env.convert_flat_state_to_composite(st))
all_state_composite = pd.DataFrame(tmp)
all_state_composite

# %% [markdown]
# ## Visualization

# %%
plotting.plot_heatmap(matrix=qtable, title="Q-table")

# %%
plotting.plot_states_actions_distribution(all_states, all_actions)

# %%
plotting.plot_steps_and_rewards(res)

# %%
plotting.plot_q_values_maps(qtable, env.rows, env.cols, CONTEXTS_LABELS)

# %%
plotting.plot_rotated_q_values_maps(qtable, env.rows, env.cols, CONTEXTS_LABELS)

# %%
plotting.plot_location_count(
    all_state_composite,
    tiles_locations=env.tiles_locations,
    cols=env.cols,
    rows=env.rows,
    cues=None,
    contexts_labels=None,
)

# %%
plotting.plot_location_count(
    all_state_composite,
    tiles_locations=env.tiles_locations,
    cols=env.cols,
    rows=env.rows,
    cues=Cues,
    contexts_labels=CONTEXTS_LABELS,
)
