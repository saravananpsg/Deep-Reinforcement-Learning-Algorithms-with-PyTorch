import copy
import random
from collections import namedtuple

import gym
import numpy as np
from gym import spaces

from Environments.Base_Environment import Base_Environment

class Bit_Flipping_Environment(gym.Env):
    environment_name = "Bit Flipping Game"

    def __init__(self, environment_dimension=20):

        self.action_space = spaces.Discrete(environment_dimension)
        self.observation_space = spaces.Dict(dict(
            desired_goal=spaces.Box(0, 1, shape=(environment_dimension,), dtype='float32'),
            achieved_goal=spaces.Box(0, 1, shape=(environment_dimension,), dtype='float32'),
            observation=spaces.Box(0, 1, shape=(environment_dimension,), dtype='float32'),
        ))

        self.seed()

        self.spec = namedtuple('spec', 'reward_threshold trials max_episode_steps')
        self.spec.reward_threshold = 0.0
        self.spec.trials = 50
        self.spec.max_episode_steps = environment_dimension

        self.environment_dimension = environment_dimension
        self.reward_for_achieving_goal = self.environment_dimension
        self.step_reward_for_not_achieving_goal = -1

    def reset(self):
        self.desired_goal = self.randomly_pick_state_or_goal()
        self.state = self.randomly_pick_state_or_goal()
        self.state.extend(self.desired_goal)
        self.achieved_goal = self.state[:self.environment_dimension]
        self.step_count = 0
        return {"observation": np.array(self.state[:self.environment_dimension]), "desired_goal": np.array(self.desired_goal),
                "achieved_goal": np.array(self.achieved_goal)}

    def randomly_pick_state_or_goal(self):
        return [random.randint(0, 1) for _ in range(self.environment_dimension)]

    def step(self, action):
        """Conducts the discrete action chosen and updated next_state, reward and done"""
        if type(action) is np.ndarray:
            action = action[0]
        assert action <= self.environment_dimension + 1, "You picked an invalid action"
        self.step_count += 1
        if action != self.environment_dimension + 1: #otherwise no bit is flipped
            self.next_state = copy.copy(self.state)
            self.next_state[action] = (self.next_state[action] + 1) % 2
        if self.goal_achieved(self.next_state):
            self.reward = self.reward_for_achieving_goal
            self.done = True
        else:
            self.reward = self.step_reward_for_not_achieving_goal
            if self.step_count >= self.environment_dimension:
                self.done = True
            else:
                self.done = False
        self.achieved_goal = self.next_state[:self.environment_dimension]
        self.state = self.next_state

        return {"observation": np.array(self.next_state[:self.environment_dimension]),
                "desired_goal": np.array(self.desired_goal), "achieved_goal": np.array(self.achieved_goal)}, self.reward, self.done, {}

    def goal_achieved(self, next_state):
        return next_state[:self.environment_dimension] == next_state[-self.environment_dimension:]

    def compute_reward(self, achieved_goal, desired_goal, info):



        if (achieved_goal == desired_goal).all():
            reward = self.reward_for_achieving_goal
        else:
            reward = self.step_reward_for_not_achieving_goal

        print("Achieved goal {} -- desired goal {} -- reward {}".format(achieved_goal, desired_goal, reward))
        return reward

    # def get_action_size(self):
    #     return self.environment_dimension + 1
    #
    # def get_state_size(self):
    #     return len(self.state)
    #
    # def get_state(self):
    #     return np.array(self.state)
    #
    # def get_next_state(self):
    #     return np.array(self.next_state)
    #
    # def get_reward(self):
    #     return self.reward
    #
    # def get_done(self):
    #     return self.done
    #
    # def get_desired_goal(self):
    #     return self.desired_goal
    #
    # def get_achieved_goal(self):
    #     return self.achieved_goal
    #
    # def get_reward_for_achieving_goal(self):
    #     return self.reward_for_achieving_goal
    #
    # def get_step_reward_for_not_achieving_goal(self):
    #     return self.step_reward_for_not_achieving_goal
    #
    # def get_max_steps_per_episode(self):
    #     return self.environment_dimension
    #
    # def get_action_types(self):
    #     return "DISCRETE"
    #
    # def get_score_to_win(self):
    #     return 0
    #
    # def get_rolling_period_to_calculate_score_over(self):
    #     return 50
    #
