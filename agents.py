import numpy as np
import math

class AgentQ:
    def __init__(self, SPD, gw, options, num_options, policy="epsilon_greedy", epsilon=0.01, alpha=0.2, gamma=0.99):
        self.gw = gw
        self.options = options
        self.num_options = num_options
        self.num_actions = 4 + self.num_options
        self.q_table = np.zeros(shape=(self.gw.grid_width * self.gw.grid_height, 4 + self.num_options))
        self.q_table = self.q_table.tolist()
        self.policy = policy
        self.epsilon = epsilon
        self.alpha = alpha
        self.gamma = gamma
        print('alpha: ', self.alpha,'gamma: ', self.gamma)
        self.one_m_alpha = (1 - self.alpha)
        self.episode = 0
        self.state_count_mat = np.zeros(len(self.q_table))

    def take_random_action(self, state, act_randomly, used_option_in=False):
        rnd = np.random.random()
        eps = 0.1
        if act_randomly and rnd <= eps: #0.15
            if used_option_in == True:
                action = np.random.randint(0, 4)
            else:
                if self.num_actions > 4:
                    v = 0.1
                    rnd2 = np.random.random()
                    if rnd2 >= v:
                        action = np.random.randint(0, 4)
                    else:
                        action = np.random.randint(4, self.num_actions)
                else:
                    action = np.random.randint(0, self.num_actions)

        else:

            if used_option_in == True:
                q_values_of_state = self.q_table[state][0:4]
            else:
                q_values_of_state = self.q_table[state]
            max_val = max(q_values_of_state)
            arg_lists = []
            option_arg_lists = []
            for i in range(0,len(q_values_of_state)):
                if q_values_of_state[i] == max_val:
                    if i >= 4:
                        option_arg_lists.append(i)
                    else:
                        arg_lists.append(i)

            if (len(arg_lists) >= 1 and len(option_arg_lists)) >= 1:
                rnd3 = np.random.random()
                v = 0.1
                if rnd3 >= v:
                    action = arg_lists[np.random.randint(0,len(arg_lists))]
                else:
                    action = option_arg_lists[np.random.randint(0, len(option_arg_lists))]

            elif len(arg_lists) >= 1:
                action = arg_lists[np.random.randint(0,len(arg_lists))]
            else:
                action = option_arg_lists[np.random.randint(0, len(option_arg_lists))]

        return action


    def update_q_values(self, old_state,new_state,reward,done,action):
        if done:
            current_q_value = self.q_table[old_state][action]
            self.q_table[old_state][action] = (self.one_m_alpha) * current_q_value + self.alpha * (reward)
        else:
            max_q_value_in_new_state = max(self.q_table[new_state])
            current_q_value = self.q_table[old_state][action]
            self.q_table[old_state][action] = (self.one_m_alpha) * current_q_value + self.alpha * (
                    reward + self.gamma * max_q_value_in_new_state)

    def update_q_values_option(self, old_state,new_state,reward,done,option):
        #alpha = 1 - self.alpha
        alpha = 0.2
        if done:
            current_q_value = self.q_table[old_state][option]
            self.q_table[old_state][option] = (1-alpha) * current_q_value + alpha * (reward)
        else:
            max_q_value_in_new_state = max(self.q_table[new_state])
            current_q_value = self.q_table[old_state][option]
            self.q_table[old_state][option] = (1-alpha) * current_q_value + alpha * (
                    reward + self.gamma * max_q_value_in_new_state)


    def update_q_values_cust_df(self, old_state,new_state,reward,done,action, gamma_iter):
        #alpha = math.pow(self.alpha, gamma_iter)
        alpha = self.alpha
        if done:
            current_q_value = self.q_table[old_state][action]
            self.q_table[old_state][action] = (1 - alpha) * current_q_value + alpha * (reward)
        else:
            max_q_value_in_new_state = max(self.q_table[new_state])
            current_q_value = self.q_table[old_state][action]
            self.q_table[old_state][action] = (1 - alpha) * current_q_value + alpha * (
                    reward + max_q_value_in_new_state)

class Option_AgentQ:
    def __init__(self, gw, option_state, num_options,SPD, policy="epsilon_greedy", epsilon=0.05, alpha=0.3, gamma=1):
        self.gw = gw
        self.option_state = option_state
        self.num_options = num_options
        print('self.num_options: ', self.num_options)
        self.num_actions = 4 + self.num_options
        self.q_table = np.zeros(shape=(self.gw.grid_width * self.gw.grid_height, 4 + self.num_options))
        self.q_table = self.q_table.tolist()
        self.policy = policy
        self.epsilon = epsilon
        self.alpha = alpha
        self.gamma = gamma
        self.one_m_alpha = (1 - self.alpha)
        self.SPD = SPD
        self.option_type = 'normal'

    def take_random_action(self, state, act_randomly, used_option_in=False):
        rnd = np.random.random()
        if act_randomly and rnd <= 0.4: #0.15
            if used_option_in == True:
                action = np.random.randint(0, 4)
            else:
                if rnd <= 0.1:   #0.075
                    action = 4
                else:
                    action = np.random.randint(0, self.num_actions)
        else:
            if used_option_in == True:
                q_values_of_state = self.q_table[state][0:4]
            else:
                q_values_of_state = self.q_table[state]
            max_val = max(q_values_of_state)
            arg_lists = []
            for i in range(0,len(q_values_of_state)):
                if q_values_of_state[i] == max_val:
                    arg_lists.append(i)
            action = arg_lists[np.random.randint(0,len(arg_lists))]
        return action

    def update_q_values(self, old_state,new_state,reward,done,action):
        if done:
            current_q_value = self.q_table[old_state][action]
            self.q_table[old_state][action] = (self.one_m_alpha) * current_q_value + self.alpha * (reward)
        else:
            max_q_value_in_new_state = self.SPD[new_state][self.option_state]
            current_q_value = self.q_table[old_state][action]
            self.q_table[old_state][action] = (self.one_m_alpha) * current_q_value + self.alpha * (
                    reward + self.gamma * max_q_value_in_new_state)