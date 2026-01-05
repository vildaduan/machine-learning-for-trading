""""""  		  	   		 	 	 			  		 			     			  	 
"""  		  	   		 	 	 			  		 			     			  	 
Template for implementing QLearner  (c) 2015 Tucker Balch  		  	   		 	 	 			  		 			     			  	 
  		  	   		 	 	 			  		 			     			  	 
Copyright 2018, Georgia Institute of Technology (Georgia Tech)  		  	   		 	 	 			  		 			     			  	 
Atlanta, Georgia 30332  		  	   		 	 	 			  		 			     			  	 
All Rights Reserved  		  	   		 	 	 			  		 			     			  	 
  		  	   		 	 	 			  		 			     			  	 
Template code for CS 4646/7646  		  	   		 	 	 			  		 			     			  	 
  		  	   		 	 	 			  		 			     			  	 
Georgia Tech asserts copyright ownership of this template and all derivative  		  	   		 	 	 			  		 			     			  	 
works, including solutions to the projects assigned in this course. Students  		  	   		 	 	 			  		 			     			  	 
and other users of this template code are advised not to share it with others  		  	   		 	 	 			  		 			     			  	 
or to make it available on publicly viewable websites including repositories  		  	   		 	 	 			  		 			     			  	 
such as github and gitlab.  This copyright statement should not be removed  		  	   		 	 	 			  		 			     			  	 
or edited.  		  	   		 	 	 			  		 			     			  	 
  		  	   		 	 	 			  		 			     			  	 
We do grant permission to share solutions privately with non-students such  		  	   		 	 	 			  		 			     			  	 
as potential employers. However, sharing with other current or future  		  	   		 	 	 			  		 			     			  	 
students of CS 7646 is prohibited and subject to being investigated as a  		  	   		 	 	 			  		 			     			  	 
GT honor code violation.  		  	   		 	 	 			  		 			     			  	 
  		  	   		 	 	 			  		 			     			  	 
-----do not edit anything above this line---  		  	   		 	 	 			  		 			     			  	 
  		  	   		 	 	 			  		 			     			  	 
Student Name: Tucker Balch (replace with your name)  		  	   		 	 	 			  		 			     			  	 
GT User ID: wduan35 (replace with your User ID)  		  	   		 	 	 			  		 			     			  	 
GT ID: 903837798 (replace with your GT ID)  		  	   		 	 	 			  		 			     			  	 
"""  		  	   		 	 	 			  		 			     			  	 
  		  	   		 	 	 			  		 			     			  	 
import random as rand  		  	   		 	 	 			  		 			     			  	 
  		  	   		 	 	 			  		 			     			  	 
import numpy as np




class QLearner(object):  		  	   		 	 	 			  		 			     			  	 
    """  		  	   		 	 	 			  		 			     			  	 
    This is a Q learner object.  		  	   		 	 	 			  		 			     			  	 
  		  	   		 	 	 			  		 			     			  	 
    :param num_states: The number of states to consider.  		  	   		 	 	 			  		 			     			  	 
    :type num_states: int  		  	   		 	 	 			  		 			     			  	 
    :param num_actions: The number of actions available..  		  	   		 	 	 			  		 			     			  	 
    :type num_actions: int  		  	   		 	 	 			  		 			     			  	 
    :param alpha: The learning rate used in the update rule. Should range between 0.0 and 1.0 with 0.2 as a typical value.  		  	   		 	 	 			  		 			     			  	 
    :type alpha: float  		  	   		 	 	 			  		 			     			  	 
    :param gamma: The discount rate used in the update rule. Should range between 0.0 and 1.0 with 0.9 as a typical value.  		  	   		 	 	 			  		 			     			  	 
    :type gamma: float  		  	   		 	 	 			  		 			     			  	 
    :param rar: Random action rate: the probability of selecting a random action at each step. Should range between 0.0 (no random actions) to 1.0 (always random action) with 0.5 as a typical value.  		  	   		 	 	 			  		 			     			  	 
    :type rar: float  		  	   		 	 	 			  		 			     			  	 
    :param radr: Random action decay rate, after each update, rar = rar * radr. Ranges between 0.0 (immediate decay to 0) and 1.0 (no decay). Typically 0.99.  		  	   		 	 	 			  		 			     			  	 
    :type radr: float  		  	   		 	 	 			  		 			     			  	 
    :param dyna: The number of dyna updates for each regular update. When Dyna is used, 200 is a typical value.  		  	   		 	 	 			  		 			     			  	 
    :type dyna: int  		  	   		 	 	 			  		 			     			  	 
    :param verbose: If “verbose” is True, your code can print out information for debugging.  		  	   		 	 	 			  		 			     			  	 
    :type verbose: bool  		  	   		 	 	 			  		 			     			  	 
    """

    def author(self):
        """
        :return: The GT username of the student
        :rtype: str
        """
        return "wduan35"  # replace tb34 with your Georgia Tech username.

    def gtid(self):
        """
        :return: The GT ID of the student
        :rtype: int
        """
        return 903837798  # replace with your GT ID number

    def __init__(self, num_states=100, num_actions=4, alpha=0.2, gamma=0.9,
                 rar=0.5, dyna=0, radr=0.99, verbose=False):
        self.verbose = verbose
        self.num_actions = num_actions
        self.s = 0  # Current state
        self.a = 0  # Current action
        self.num_states = num_states
        self.alpha = alpha
        self.gamma = gamma
        self.rar = rar
        self.radr = radr
        self.dyna = dyna

        # Initialize the Q-table with random values between -1.0 and 1.0
        self.Q = np.random.uniform(low=-1.0, high=1.0, size=(num_states, num_actions))
        # Dyna-Q initiate
        self.model = {}  # Environment model: (s, a) -> (s', r)
        self.visited_states_actions = set()  # Track visited (s, a) pairs

    def querysetstate(self, s):
        """
        Updates the current state without modifying the Q-table.
        Returns the action selected based on greedy approach.

        :param s: The state to update.
        :returns: Action chosen based on greedy policy.
        """
        self.s = s
        action = rand.randint(0, self.num_actions - 1)
        if rand.random() > self.rar:
            action = np.argmax(self.Q[s, :])

        if self.verbose:
            print(f"s = {s}, a = {action}")

        return action

    def query(self, s_prime, r):
        """
        Updates the Q-table based on the new state (s_prime) and reward (r),
        and returns the next action using an epsilon-greedy strategy.

        :param s_prime: The next state after taking action.
        :param r: The reward received after taking the action.
        :returns: Next action selected based on greedy policy.
        """
        # Update Q-table using the Q-learning formula
        self.Q[self.s, self.a] = (1 - self.alpha) * self.Q[self.s, self.a] + self.alpha * (
                    r + self.gamma * np.max(self.Q[s_prime, :]))

        # Dyna-Q updates (simulated experiences)
        if self.dyna > 0:
            # Update the environment model with real experience
            self.model[(self.s, self.a)] = (s_prime, r)
            self.visited_states_actions.add((self.s, self.a))

            for _ in range(self.dyna):
                s_dyna, a_dyna = rand.choice(list(self.visited_states_actions))
                s_prime_dyna, r_dyna = self.model[(s_dyna, a_dyna)]

                self.Q[s_dyna, a_dyna] += self.alpha * (
                            r_dyna + self.gamma * np.max(self.Q[s_prime_dyna, :]) - self.Q[s_dyna, a_dyna])
        # Choose next action
        if rand.random() <= self.rar:
            action = rand.randint(0, self.num_actions - 1)
        else:
            action = np.argmax(self.Q[s_prime, :])

        # Decay random action rate
        self.rar *= self.radr

        # Update current state and action
        self.s = s_prime
        self.a = action

        if self.verbose:
            print(f"s = {s_prime}, a = {action}, r = {r}")

        return action

    #non dyna version

    # def __init__(self, num_states=100, num_actions=4, alpha=0.2, gamma=0.9,
    #              rar=0.5, dyna=0, radr=0.99, verbose=False):
    #     self.verbose = verbose
    #     self.num_actions = num_actions
    #     self.s = 0  # Current state
    #     self.a = 0  # Current action
    #     self.num_states = num_states
    #     self.alpha = alpha
    #     self.gamma = gamma
    #     self.rar = rar
    #     self.radr = radr
    #
    #     # Initialize the Q-table with random values between -1.0 and 1.0
    #     self.Q = np.random.uniform(low=-1.0, high=1.0, size=(num_states, num_actions))
    #
    # def querysetstate(self, s):
    #     """
    #     Updates the current state without modifying the Q-table.
    #     Returns the action selected based on epsilon-greedy approach.
    #
    #     :param s: The state to update.
    #     :returns: Action chosen based on epsilon-greedy policy.
    #     """
    #     self.s = s
    #     action = rand.randint(0, self.num_actions - 1)
    #     if rand.random() > self.rar:
    #         action = np.argmax(self.Q[s, :])
    #
    #     if self.verbose:
    #         print(f"s = {s}, a = {action}")
    #
    #     return action
    #
    # def query(self, s_prime, r):
    #     """
    #     Updates the Q-table based on the new state (s_prime) and reward (r),
    #     and returns the next action using an epsilon-greedy strategy.
    #
    #     :param s_prime: The next state after taking action.
    #     :param r: The reward received after taking the action.
    #     :returns: Next action selected based on epsilon-greedy policy.
    #     """
    #     # Update Q-table using the Q-learning formula
    #     self.Q[self.s, self.a] = (1 - self.alpha) * self.Q[self.s, self.a] + self.alpha * (
    #                 r + self.gamma * np.max(self.Q[s_prime, :]))
    #
    #     # Choose next action using epsilon-greedy
    #     if rand.random() <= self.rar:
    #         action = rand.randint(0, self.num_actions - 1)  # Explore
    #     else:
    #         action = np.argmax(self.Q[s_prime, :])  # Exploit
    #
    #     # Decay random action rate
    #     self.rar *= self.radr
    #
    #     # Update current state and action
    #     self.s = s_prime
    #     self.a = action
    #
    #     if self.verbose:
    #         print(f"s = {s_prime}, a = {action}, r = {r}")
    #
    #     return action





  		  	   		 	 	 			  		 			     			  	 
if __name__ == "__main__":
    print("Remember Q from Star Trek? Well, this isn't him")
