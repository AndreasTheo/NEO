import numpy as np
import pickle
from sklearn.cluster import SpectralClustering
import networkx as nx
import math
import copy

def create_graphs(env_name, matrix=None):
    if matrix is None:
        with open(env_name, 'rb') as filehandle:
            matrix = np.array(pickle.load(filehandle))

    for i in range(len(matrix)):
        for k in range(len(matrix[0])):
            if matrix[i][k] == 0:
                matrix[i][k] = 1
            else:
                matrix[i][k] = 0

    node_length = len(matrix) * len(matrix[0])
    rb_vec = np.zeros((node_length, node_length))  #
    flat_mat = matrix.flatten()
    mat_pos = []
    # matrix to pos:
    offset_pos_ = 5
    for i in range(len(matrix)):
        for k in range(len(matrix[0])):
            mat_pos.append([i + offset_pos_, k + offset_pos_])
            pass
    l = len(matrix[0])

    for i in range(node_length):
        if flat_mat[i] == 1:
            if i + 1 < node_length: #if state to the left is not wall
                if (i + 1) % l != 0:
                    if flat_mat[i + 1] == 1:
                        rb_vec[i][i + 1] = 1

            if i + l < node_length: #if state below is not wall
                if flat_mat[i + l] == 1:
                    rb_vec[i][i + l] = 1
                else:
                    rb_vec[i][i] = 1

    mat_pos = np.array(mat_pos)
    G = nx.DiGraph()
    G2 = nx.DiGraph()
    new_flat_mat = np.zeros(node_length)
    for i in range(node_length):
        G2.add_node(i)
        G2.nodes[i]['pos'] = mat_pos[i]
        if flat_mat[i] == 1:
            G.add_node(i)
            G.nodes[i]['pos'] = mat_pos[i]

    for i in range(node_length):
        s_i = mat_pos[i]
        has_edges = False
        for k in range(node_length):
            if i != k:
                if rb_vec[i][k] == 1:
                    new_flat_mat[i] = 1
                    new_flat_mat[k] = 1
                    has_edges = True
                    G2.add_edge(i, k, weight=1)
                    G.add_edge(i, k, weight=1)
                    s_k = mat_pos[k]
            # if i == k:
            #     for j in range(0,int(rb_vec[i][i])):
            #         G2.add_edge(i,i,weight=1)

    return G, G2

def convert_to_degree_row(row_M):
    #uniform_prob = 1 / np.sum(row_M)
    adding_row = np.sum(row_M)
    for k in range(len(row_M)):
        if row_M[k] > 0:
            row_M[k] = row_M[k] / adding_row
    return row_M

def create_sc(G, cluster_num):
    M_copy = nx.adjacency_matrix(G).todense()
    sc = SpectralClustering(cluster_num, affinity='precomputed', n_init=100)
    sc.fit(M_copy)
    return sc


def create_random_stateset_from_cluster(cluster_num, clusters, G):
    random_state_states = []
    for i in range(cluster_num):
        g = 0
        singe_label_list = []
        for node in G.nodes:
            if clusters.labels_[g] == i:
                singe_label_list.append(node)
            g += 1
        random_gs = np.random.choice(singe_label_list)
        random_state_states.append(random_gs)
    print('random_state_states: ', random_state_states)
    return random_state_states

def create_random_state_set_with_spectral_clustering(G,cluster_num):
    sc = create_sc(G, cluster_num)
    random_state_set = create_random_stateset_from_cluster(cluster_num,sc, G)
    return random_state_set


def moving_avg(data, window_size):
    i = 0
    moving_averages = []
    while i < len(data) - window_size + 1:
        this_window = data[i: i + window_size]
        window_average = sum(this_window) / window_size
        moving_averages.append(window_average)
        i += 1
    return moving_averages

from agents import Option_AgentQ
# def create_option(option_goal, gw, SPD):
#     option_agent = Option_AgentQ(gw, option_goal,0,SPD, gamma=1)
#     e = 0
#     print('m', option_goal)
#     print(gw.grid_height)
#     os_row = math.floor(option_goal / gw.grid_height)
#     os_col = option_goal % gw.grid_width
#     #print('os_row: ', os_row, 'os_col: ', os_col)
#     act_randomly = True
#     while (e < 5000):
#         if e > 4500:
#             act_randomly = False
#         steps = 0
#         start_state = gw.sample_random_state()
#         ss_row = math.floor(start_state / gw.grid_height)
#         ss_col = start_state % gw.grid_width
#         state = gw.reset_world(ss_row, ss_col, os_row, os_col)  # 28
#         for i in range(300):
#             steps += 1
#             action = option_agent.take_random_action(state, act_randomly,True)
#             if e > 4500:
#                 next_state, reward, done = gw.step_option_v2(action)
#             else:
#                 next_state, reward, done = gw.step_option(action)
#                 option_agent.update_q_values(state, next_state, reward, done, action)
#             state = next_state
#             if done:
#                 break
#         if act_randomly == False:
#             print('option_ e: ', e, 'steps: ', steps, 'act_randomly: ', act_randomly, 'start_state: ', start_state, 'option_goal: ', option_goal)
#         e += 1
#     #round option value function to allow random choice between optimal paths
#     option_agent.q_table = np.round(option_agent.q_table,decimals=0)
#     return option_agent



# def create_option(option_goal, gw, SPD):
#     option_agent = Option_AgentQ(gw, option_goal,0,SPD, gamma=1)
#     e = 0
#     print('m', option_goal)
#     print(gw.grid_height)
#     os_row = math.floor(option_goal / gw.grid_height)
#     os_col = option_goal % gw.grid_width
#     #print('os_row: ', os_row, 'os_col: ', os_col)
#     act_randomly = True
#     while (e < 5000):
#         if e > 4500:
#             act_randomly = False
#         steps = 0
#         start_state = gw.sample_random_state()
#         ss_row = math.floor(start_state / gw.grid_height)
#         ss_col = start_state % gw.grid_width
#         state = gw.reset_world(ss_row, ss_col, os_row, os_col)  # 28
#         for i in range(300):
#             steps += 1
#             action = option_agent.take_random_action(state, act_randomly,True)
#             if e > 4500:
#                 next_state, reward, done = gw.step_option_v2(action)
#             else:
#                 next_state, reward, done = gw.step_option(action)
#                 option_agent.update_q_values(state, next_state, reward, done, action)
#             state = next_state
#             if done:
#                 break
#         if act_randomly == False:
#             print('option_ e: ', e, 'steps: ', steps, 'act_randomly: ', act_randomly, 'start_state: ', start_state, 'option_goal: ', option_goal)
#         e += 1
#     #round option value function to allow random choice between optimal paths
#     option_agent.q_table = np.round(option_agent.q_table,decimals=0)
#     return option_agent

def create_option(option_goal, gw, SPD):
    option_agent = Option_AgentQ(gw, option_goal, 0, SPD, gamma=1)
    for node in gw.G.nodes:
            state = convert1d_to_2d(node, gw)
            next_states = get_next_states(state,gw)
            act = 0
            for next_state in next_states:
                #print(node, next_state, option_goal)
                #print('np.shape: ', np.shape(option_agent.q_table))
                #print(SPD[next_state][option_goal])
                option_agent.q_table[node][act] = SPD[next_state][option_goal]
                act+=1
    # round option value function to allow random choice between optimal paths
    option_agent.q_table = np.round(option_agent.q_table, decimals=0)
    return option_agent

def get_next_states(state,gw):
        agent_pos = [state[0], state[1]]
        one = set_agent_pos([-1, 0],agent_pos,gw)  # left
        two = set_agent_pos([1, 0],agent_pos,gw)  # right
        three = set_agent_pos([0, -1],agent_pos,gw)  # down
        four = set_agent_pos([0, 1],agent_pos,gw)  # up
        one = one[0] * gw.grid_width + one[1]
        two = two[0] * gw.grid_width + two[1]
        three = three[0] * gw.grid_width + three[1]
        four = four[0] * gw.grid_width + four[1]
        return [one, two, three, four]

def set_agent_pos(dir,agent_pos,gw):
        new_pos = np.copy(agent_pos)
        new_pos[0] += dir[0]
        new_pos[1] += dir[1]
        if (new_pos[0] < 0 or new_pos[0] > len(gw.grid) - 1):
            return agent_pos
        elif (new_pos[1] < 0 or (new_pos[1] > len(gw.grid[0]) - 1)):
            return agent_pos
        elif (gw.grid[new_pos[0]][new_pos[1]] == 1):
                return agent_pos
        else:
            return new_pos



def convert1d_to_2d(c_state, gw):
    ss_row = math.floor(c_state / gw.grid_height)
    ss_col = c_state % gw.grid_width
    c_state_2d = [ss_row, ss_col]
    return copy.deepcopy(c_state_2d)


def calculate_shortest_path_matrix(G, include_all_paths = True):
    SP_list = []
    l = len(list(G.nodes))


    for r_state in range(l):
        SP_list.append([])
        for c_state in range(l):
            SP_list[r_state].append([])

    SPD = np.empty(  (l, l)  )
    print('calculating shortest path distances...')
    for r_state in range(l):
        for c_state in range(l):
            try:
                if include_all_paths:
                    SP_list[r_state][c_state].append([p for p in nx.all_shortest_paths(G, source=r_state, target=c_state)])
                SPD[r_state][c_state] = -nx.shortest_path_length(G, source=r_state, target=c_state)
                #SPD[r_state][c_state][1] = [p for p in nx.all_shortest_paths(G2, source=r_state, target=c_state)]
                #print('shortest paths: ', [p for p in nx.all_shortest_paths(G2, source=r_state, target=c_state)])
            except:
                SPD[r_state][c_state] = 0
                if include_all_paths:
                    SP_list[r_state][c_state] = [[[9999],[9999]]]

    if include_all_paths:
        return SPD, SP_list
    else:
        return SPD

# def get_all_shortest_path_data(env_name, M, G2):
#     try:
#         with open(env_name + '.SPD.data', 'rb') as handle:
#             SPD = pickle.load(handle)
#         with open(env_name + '.SP_list.data', 'rb') as handle:
#             SP_list = pickle.load(handle)
#         with open(env_name + '.SP_occ_list.data', 'rb') as handle:
#             state_occ_in_sp_list = pickle.load(handle)
#
#         ########### OVERRIDE FOR WHEN STATE OCC CAL IS NOT BEING COMPUTED IN TEST ################
#         # with open(env_name + '.SPD.data', 'rb') as handle:
#         #     SPD = pickle.load(handle)
#         # with open(env_name + '.SPD.data', 'rb') as handle:
#         #     SP_list = pickle.load(handle)
#         # with open(env_name + '.SPD.data', 'rb') as handle:
#         #     state_occ_in_sp_list = pickle.load(handle)
#
#     except OSError as err:
#         SPD, SP_list = calculate_shortest_path_matrix(M,G2)
#         state_occ_in_sp_list = np.zeros((len(M), len(M), len(M)))
#         for i in range(len(M)):
#             print('i: ', i)
#             for j in range(len(M)):
#                 for k in range(len(M)):
#                     state_occ_in_sp_list[i][j][k] = sum(x.count(k) for x in SP_list[i][j][0])
#                     #state_occ_in_sp_list[i][j][k] = 0
#
#         with open(env_name + '.SPD.data', 'wb') as handle:
#             pickle.dump(SPD, handle, protocol=pickle.HIGHEST_PROTOCOL)
#         with open(env_name + '.SP_list.data', 'wb') as handle:
#             pickle.dump(SP_list, handle, protocol=pickle.HIGHEST_PROTOCOL)
#         with open(env_name + '.SP_occ_list.data', 'wb') as handle:
#             pickle.dump(state_occ_in_sp_list, handle, protocol=pickle.HIGHEST_PROTOCOL)
#         print('saved..')
#     return SPD, SP_list, state_occ_in_sp_list


def get_all_shortest_path_dists(env_name, G):
    try:
        with open(env_name + '.SPD.data', 'rb') as handle:
            SPD = pickle.load(handle)
    except OSError as err:
        SPD = calculate_shortest_path_matrix(G, False)

        with open(env_name + '.SPD.data', 'wb') as handle:
            pickle.dump(SPD, handle, protocol=pickle.HIGHEST_PROTOCOL)

        print('saved..')
    return SPD


def convert2d_to_1d(x_pos,y_pos,gw):
    new_state = x_pos * gw.grid_width + y_pos
    return new_state

