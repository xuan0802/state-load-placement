# -*- coding: utf-8 -*-
"""
Created on Thu Nov  9 17:11:44 2017

@author: xuan
"""
from gurobipy import Model, GRB
import pandas as pd
from math import sqrt
from copy import deepcopy
import ujson
from contants import *
from ultilities import prod
import time


# define optimization models
# optimize state transfer
def optimize_state_transfer(n, h, u):
    # create a model
    m = Model('state transfer')
    # create decision variables
    x = m.addVars(sa, sa, vtype=GRB.BINARY, name='x')
    y = m.addVars(sa, dc, vtype=GRB.BINARY, name='y')
    
    # add constraints
    # x is symmetric
    m.addConstrs((x[i, j] == x[j, i] for i in sa for j in sa), 'symmetric constraint')
    # Two service areas cant use the same stateful functions when x[i,j] = 0
    m.addConstrs((y[i, t] + y[j, t] <= x[i, j] + 1 for i in sa for j in sa for t in dc), 'x = 0 constraint')
    # Two service areas use the same stateful functions when x[i,j] = 1
    m.addConstrs(((y[i, t] - y[j, t] <= 1 - x[i, j]) for i in sa for j in sa for t in dc), 'x = 1 constraint')
    # Each should be at least managed by one dc
    m.addConstrs((sum(y[i, t] for t in dc) == 1 for i in sa), 'one dc for one sa')
    # high availability constraint
    m.addConstr(sum((1-x[i, j]) for i in sa for j in sa if i != j) >= 1, 'ha')
    # maximum traffic load constraint
    m.addConstr((sum(y[i, dc[0]]*n*(L_sig + u*L_session) for i in sa) <= Traffic_max), 'load maximum constraint')
    # dc0 will have the most heavy load
    for t in dc:
        if t != dc[0]:
            m.addConstr(sum(y[i, t]*n*(L_sig + u*L_session) for i in sa) <=
                        sum(y[i, dc[0]]*n*(L_sig + u*L_session) for i in sa), 'less than max load')
    
    # Objective function
    m.setObjective(sum(h*(1-x[i, j]) for i in sa for j in sa if i != j), GRB.MINIMIZE)
    
    # run model
    m.optimize()
    # check model feasible or not
    if m.getAttr('status') == GRB.INFEASIBLE:
        return 'infeasible'

    # Calculate performance metrics
    # traffic load on stateful functions
    traffic_load = sum(getattr(y[i, dc[0]], 'X')*n*(L_sig + u*L_session) for i in sa)
    
    # state transfer frequency
    state_transfer = sum(h*(1-getattr(x[i, j], 'X')) for i in sa for j in sa if i != j)
    
    # number of function
    num_func = M_dc - sum(prod(1 - getattr(y[i, t], 'X') for i in sa) for t in dc)
    # total metrics
    total_metrics = [u, h, u, state_transfer, traffic_load, num_func]
    
    # utopia point, nadir point
    best_state = state_transfer
    worst_load = traffic_load
    
    return total_metrics, best_state, worst_load


# optimize traffic load
def optimize_traffic_load(n, h, u):
    # create a model
    m = Model('traffic load')
    # create decision variables
    x = m.addVars(sa, sa, vtype=GRB.BINARY, name='x')
    y = m.addVars(sa, dc, vtype=GRB.BINARY, name='y')
    
    # add constraints
    # x is symmetric
    m.addConstrs((x[i, j] == x[j, i] for i in sa for j in sa), 'symmetric constraint')
    # Two service areas cant use the same stateful functions when x[i,j] = 0
    m.addConstrs((y[i, t] + y[j, t] <= x[i, j] + 1 for i in sa for j in sa for t in dc), 'x = 0 constraint')
    # Two service areas use the same stateful functions when x[i,j] = 1
    m.addConstrs(((y[i, t] - y[j, t] <= 1 - x[i, j]) for i in sa for j in sa for t in dc), 'x = 1 constraint')
    # Each should be at least managed by one dc
    m.addConstrs((sum(y[i, t] for t in dc) == 1 for i in sa), 'one dc for one sa')
    # high availability constraint
    m.addConstr(sum((1-x[i, j]) for i in sa for j in sa if i != j) >= 1, 'ha')
    # maximum state transfer frequency
    m.addConstr(sum(h*(1 - x[i, j]) for i in sa for j in sa if i != j) <= State_max, 'max state transfer constraint')
    # dc0 will have the most heavy load
    for t in dc:
        if t != dc[0]:
            m.addConstr(sum(y[i, t]*n*(L_sig + u*L_session) for i in sa) <=
                        sum(y[i, dc[0]]*n*(L_sig + u*L_session) for i in sa), 'less than max load')
    
    # Objective function
    # Optimize load on one cloud centers and mandate other centers to be less than
    m.setObjective(sum(y[i, dc[0]]*n*(L_sig + u*L_session) for i in sa),  GRB.MINIMIZE)

    m.optimize()
    # check model feasible or not
    if m.getAttr('status') == GRB.INFEASIBLE:
        return 'infeasible'

    # Calculate performance metrics
    # traffic load on stateful functions
    traffic_load = sum(getattr(y[i, dc[0]], 'X')*n*(L_sig + u*L_session) for i in sa)
    
    # state transfer frequency
    state_transfer = sum(h*(1-getattr(x[i, j], 'X')) for i in sa for j in sa if i != j)
    
    # number of function
    num_func = M_dc - sum(prod(1 - getattr(y[i, t], 'X') for i in sa) for t in dc)

    # total metrics
    total_metrics = [u, h, u, state_transfer, traffic_load, num_func]
    
    # utopia point, nadir point
    worst_state = state_transfer
    best_load = traffic_load
    
    return total_metrics, worst_state, best_load


# Trade off solution
def optimize_pareto(n, h, u, ju_s, ju_l, jn_s, jn_l, w):

    # check input parameters
    if ju_l == jn_l or ju_s == jn_s:
        return 'worst and best overlap'
    # create a model
    m = Model('Pareto')
    # create decision variables
    x = m.addVars(sa, sa, vtype=GRB.BINARY, name='x')
    y = m.addVars(sa, dc, vtype=GRB.BINARY, name='y')
    
    # add constraints
    # x is symmetric
    m.addConstrs((x[i, j] == x[j, i] for i in sa for j in sa), 'symmetric constraint')
    # Two service areas cant use the same stateful functions when x[i,j] = 0
    m.addConstrs((y[i, t] + y[j, t] <= x[i, j] + 1 for i in sa for j in sa for t in dc), 'x = 0 constraint')
    # Two service areas use the same stateful functions when x[i,j] = 1
    m.addConstrs(((y[i, t] - y[j, t] <= 1 - x[i, j]) for i in sa for j in sa for t in dc), 'x = 1 constraint')
    # Each should be at least managed by one dc
    m.addConstrs((sum(y[i, t] for t in dc) == 1 for i in sa), 'one dc for one sa')
    # high availability constraint
    m.addConstr(sum((1-x[i, j]) for i in sa for j in sa if i != j) >= 1, 'ha')
    # maximum state transfer frequency
    m.addConstr(sum(h*(1 - x[i, j]) for i in sa for j in sa if i != j) <= jn_s - 1, 'max state transfer constraint')
    # maximum traffic load constraint
    m.addConstr((sum(y[i, dc[0]]*n*(L_sig + u*L_session) for i in sa) <= jn_l - 1), 'load maximum constraint')
    # dc0 will have the most heavy load
    for t in dc:
        if t != dc[0]:
            m.addConstr(sum(y[i, t]*n*(L_sig + u*L_session) for i in sa) <=
                        sum(y[i, dc[0]]*n*(L_sig + u*L_session) for i in sa), 'less than max load')
    
    # Objective function
    m.setObjective((1-w)*(sum(y[i, dc[0]]*n*(L_sig + u*L_session) for i in sa)-ju_l)/(jn_l - ju_l) +
                   w*(sum(h*(1 - x[i, j]) for i in sa for j in sa if i != j)-ju_s)/(jn_s-ju_s), GRB.MINIMIZE)
    
    m.optimize()

    # check model feasible or not
    if m.getAttr('status') == GRB.INFEASIBLE:
        return 'infeasible'

    # Calculate performance metrics
    # traffic load on stateful functions
    traffic_load = sum(getattr(y[i, dc[0]], 'X')*n*(L_sig + u*L_session) for i in sa)
    
    # state transfer frequency
    state_transfer = sum(h*(1-getattr(x[i, j], 'X')) for i in sa for j in sa if i != j)
    
    # number of functions
    num_func = M_dc - sum(prod(1 - getattr(y[i, t], 'X') for i in sa) for t in dc)
    
    # total metrics
    total_metrics = [u, h, u, state_transfer, traffic_load, num_func]

    return total_metrics


# adaptive weighted sum
def adaptive_weighted_sum(n, h, u, variable_para):
    # define a set to store Pareto points
    perf_pareto_set = set()
    # define a map between Pareto point and weight
    pareto_weight_map = {}
    # solve single objective models
    perf_state, best_state, worst_load = optimize_state_transfer(n, h, u)
    perf_load, worst_state, best_load = optimize_traffic_load(n, h, u)
    perf_pareto_set.add((best_state, worst_load, perf_state[5]))
    perf_pareto_set.add((worst_state, best_load, perf_load[5]))

    # define initial step size
    n_init = 10
    weight_list = [x/n_init for x in range(n_init) if x != 0]
    # find initial Pareto points
    for weight in weight_list:
        temp = optimize_pareto(n, h, u, best_state, best_load, worst_state, worst_load, weight)
        if temp == 'infeasible' or temp == 'worst and best overlap':
            print("pass")
        else:
            perf_pareto_set.add((temp[3], temp[4], temp[5]))
            if (temp[3], temp[4], temp[5]) in pareto_weight_map:
                pareto_weight_map[(temp[3], temp[4], temp[5])].append(weight)
            else:
                pareto_weight_map[(temp[3], temp[4], temp[5])] = list()
                pareto_weight_map[(temp[3], temp[4], temp[5])].append(weight)

    # sort Pareto points in the ascending order of state
    perf_pareto_list = list(perf_pareto_set)
    perf_pareto_list.sort(key=lambda x: x[0])

    # calculate the number of further refinements
    segment_list = list()
    n_i_list = list()
    C = 10
    for i in range(len(perf_pareto_list) - 1):
        segment_list.append(sqrt(pow(perf_pareto_list[i+1][0] - perf_pareto_list[i][0], 2)
                          + pow(perf_pareto_list[i][1] - perf_pareto_list[i+1][1], 2)))

    segment_list_sorted = deepcopy(segment_list)
    segment_list_sorted.sort(key=lambda x: x)
    for i in range(len(segment_list)):
        n_i = round(segment_list[i]/segment_list_sorted[0])*C
        if n_i < 20:
            n_i_list.append(n_i)
        else:
            n_i_list.append(20)

    # for each region, find more Pareto optimal points
    for i in range(len(perf_pareto_list) - 1):
        weight_list = [x/n_i_list[i] for x in range(n_i_list[i]) if x != 0]
        for weight in weight_list:
            temp = optimize_pareto(n, h, u, perf_pareto_list[i][0], perf_pareto_list[i+1][1],
                                   perf_pareto_list[i+1][0], perf_pareto_list[i][1], weight)
            if temp == 'infeasible' or temp == 'worst and best overlap':
                print('pass')
            else:
                perf_pareto_set.add((temp[3], temp[4], temp[5]))

    # if variable_para == 'h':
    #     output_file(perf_pareto_set, pareto_weight_map, variable_para, h)
    # elif variable_para == 'u':
    #     output_file(perf_pareto_set, pareto_weight_map, variable_para, u)
    # elif variable_para == 'n':
    #     output_file(perf_pareto_set, pareto_weight_map, variable_para, n)


def output_file(perf_pareto_set, pareto_weight_map, variable_para, v):
    filename = "data/pareto_" + variable_para + "_" + str(v) + ".js"
    f = open(filename, 'w')
    ujson.dump(perf_pareto_set, f)
    filename = "data/pareto_weight_" + variable_para + "_" + str(v) + ".js"
    f = open(filename, 'w')
    ujson.dump(pareto_weight_map, f)


def get_running_time(n, h, u):
    running_time = dict()
    t0 = time.time()
    perf_state, best_state, worst_load = optimize_state_transfer(n, h, u)
    t1 = time.time()
    running_time['OST'] = t1 - t0
    t0 = time.time()
    perf_load_, worst_state, best_load = optimize_traffic_load(n, h, u)
    t1 = time.time()
    running_time['OTL'] = t1 - t0
    t0 = time.time()
    optimize_pareto(n, h, u, best_state, best_load, worst_state, worst_load, 0.5)
    t1 = time.time()
    running_time['PO'] = t1 - t0
    t0 = time.time()
    adaptive_weighted_sum(n, h, u, 'h')
    t1 = time.time()
    running_time['APO'] = t1 - t0
    print(running_time)


# obtain results
# handover_list = [0.5] + [5*x for x in range(20) if x != 0]
# request_list = [x for x in range(10)]
# ue_num_list = [1] + [50*x for x in range(20) if x != 0]

u_ = 5
h_ = 50
n_ = 550

get_running_time(n_, h_, u_)






