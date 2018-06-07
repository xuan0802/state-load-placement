import matplotlib.pyplot as plt
import ujson
from contants import *
import numpy as np
from ast import literal_eval


# product function
def prod(x):
    product = 1
    for i in x:
        product = product * i
    return product


def draw_pareto_front_ue_num():
    # make figures
    plt.figure()

    for n_ in ue_num_list:
        # read data
        filename = "data/pareto_n_" + str(n_) + ".js"
        f = open(filename)
        perf_pareto_list = ujson.load(f)
        # make plots
        x_data = list()
        y_data = list()

        perf_pareto_list.sort(key=lambda x: x[0])

        for i in perf_pareto_list:
            x_data.append(i[0])
            y_data.append(i[1])
        plt.plot(x_data, y_data, marker='D', markerfacecolor=line_style_map_ue[n_]['marker_color'], markersize=10,
                 linestyle='dashed', color='olive', label=line_style_map_ue[n_]['label'])
        for a in annotate_map_ue[n_].keys():
            plt.annotate(annotate_map_ue[n_][a], a)
    plt.xlabel('State Transfer Cost', fontsize='x-large')
    plt.ylabel('Traffic load', fontsize='x-large')
    plt.legend()
    plt.show()


def draw_pareto_front_handover_frequency():
    # make figures
    plt.figure()
    for h_ in handover_list:
        # read data
        filename = "data/pareto_h_" + str(h_) + ".js"
        f = open(filename)
        perf_pareto_list = ujson.load(f)
        # make plots
        x_data = list()
        y_data = list()

        perf_pareto_list.sort(key=lambda x: x[0])

        for i in perf_pareto_list:
            x_data.append(i[0])
            y_data.append(i[1])
        plt.plot(x_data, y_data, marker='D', markerfacecolor=line_style_map_handover[h_]['marker_color'], markersize=10,
                 linestyle='dashed', color='olive', label=line_style_map_handover[h_]['label'])
        for a in annotate_map_handover[h_].keys():
            plt.annotate(annotate_map_handover[h_][a], a)
    plt.xlabel('State Transfer Cost', fontsize='x-large')
    plt.ylabel('Traffic load', fontsize='x-large')
    plt.legend()
    plt.show()


def draw_pareto_front_request():
    # make figures
    plt.figure()
    for u_ in ue_num_list:
        # read data
        filename = "data/pareto_u_" + str(u_) + ".js"
        f = open(filename)
        perf_pareto_list = ujson.load(f)
        # make plots
        x_data = list()
        y_data = list()

        perf_pareto_list.sort(key=lambda x: x[0])

        for i in perf_pareto_list:
            x_data.append(i[0])
            y_data.append(i[1])
        plt.plot(x_data, y_data, marker='D', markerfacecolor=line_style_map_request[u_]['marker_color'], markersize=10,
                 linestyle='dashed', color='olive', label=line_style_map_request[u_]['label'])
        for a in annotate_map_request[u_].keys():
            plt.annotate(annotate_map_request[u_][a], a)
    plt.xlabel('State Transfer Cost', fontsize='x-large')
    plt.ylabel('Traffic load', fontsize='x-large')
    plt.legend()
    plt.show()


def draw_running_time():
    po = dict()
    po['label'] = 'PO with w=0.5'
    po['running_time'] = [0.882800817489624,  1.1198995113372803, 1.508939266204834]
    ost = dict()
    ost['label'] = 'OST'
    ost['running_time'] = [0.9020464420318604, 1.149639368057251, 2.6382675170898438]
    otl = dict()
    otl['label'] = 'OTL'
    otl['running_time'] = [0.09352946281433105, 0.12285518646240234, 0.1560497283935547]
    apo = dict()
    apo['label'] = 'APO'
    apo['running_time'] = [42.97541284561157, 45.240522384643555,  69.9119827747345]
    algorithms = list()
    algorithms.append(po)
    algorithms.append(ost)
    algorithms.append(otl)
    algorithms.append(apo)
    xtick = ['M=10', 'M=11', 'M=12']
    fig, ax = plt.subplots()
    color_list = {'PO with w=0.5':'blue', 'OST':'red', 'OTL':'green', 'APO':'olive'}
    index = np.arange(len(xtick))
    bar_width = 0.2
    opacity = 0.8
    i = 0
    for algo in algorithms:
        ax.bar(index + i * bar_width, algo['running_time'],
               bar_width, alpha=opacity, color=color_list[algo['label']], label=algo['label'])
        i = i + 1

    ax.set_xlabel('Number of cloud centers', fontsize='x-large')
    ax.set_ylabel('Running time (s)', fontsize='x-large')
    ax.set_yscale('log')
    ax.set_xticks(index + bar_width)
    ax.set_xticklabels(xtick)
    ax.legend(fontsize='large', loc="upper left")
    fig.tight_layout()
    plt.show()


def draw_performance_results_handover():
    handover_list = [0.5] + [5*x for x in range(20) if x != 0]
    OST = dict()
    OTL = dict()
    PO = dict()
    APO = dict()

    OST['state'] = []
    OTL['state'] = []
    PO['state'] = []

    OST['load'] = []
    OTL['load'] = []
    PO['load'] = []

    OST['num_func'] = []
    OTL['num_func'] = []
    PO['num_func'] = []

    for h in handover_list:
        filename = "data/pareto_" + 'h' + "_" + str(h) + ".js"
        f = open(filename)
        pareto_optimal_points = ujson.load(f)
        pareto_optimal_points.sort(key=lambda x: x[0])

        OST['state'].append(pareto_optimal_points[0][0])
        OST['load'].append(pareto_optimal_points[0][1])
        OST['num_func'].append(pareto_optimal_points[0][2])

        OTL['state'].append(pareto_optimal_points[len(pareto_optimal_points)-1][0])
        OTL['load'].append(pareto_optimal_points[len(pareto_optimal_points)-1][1])
        OTL['num_func'].append(pareto_optimal_points[len(pareto_optimal_points)-1][2])

        filename = "data/pareto_weight_" + 'h' + "_" + str(h) + ".js"
        f = open(filename)
        pareto_optimal_weight_map = ujson.load(f)
        for point in pareto_optimal_weight_map.keys():
            if 0.5 in pareto_optimal_weight_map[point]:
                p_ = literal_eval(point)
                PO['state'].append(p_[0])
                PO['load'].append(p_[1])
                PO['num_func'].append(p_[2])
                break

        print('--------------------------', h, '-----------')
        print('best state', pareto_optimal_points[0][0])
        print('worst state', pareto_optimal_points[len(pareto_optimal_points)-1][0])
        print('best load', pareto_optimal_points[len(pareto_optimal_points)-1][1])
        print('worst load', pareto_optimal_points[0][1])
        print('PO state', p_[0])
        print('PO load', p_[1])

        APO['state'] = [32.0, 320.0, 640.0, 960.0, 1280.0, 1600.0, 1920.0, 2240.0, 2560.0, 2880.0, 3200.0, 3520.0,
                        3840.0, 4160.0, 4480.0, 4800.0, 5120.0, 5440.0, 5760.0, 6080.0]
        APO['load'] = [132000.0, 132000.0, 132000.0, 132000.0, 132000.0, 132000.0, 132000.0, 132000.0,
                       132000.0, 132000.0, 132000.0, 132000.0, 132000.0, 132000.0, 132000.0, 132000.0,
                       132000.0, 132000.0, 132000.0, 165000.0]
        APO['num_func'] = [3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0,
                           3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0]
    figures = ['state', 'load', 'num_func']
    ylabel_map = {'state': 'State Transfer Cost', 'load':'Traffic Load', 'num_func':'Number of StateMF sets'}
    for fig in figures:
        plt.plot(handover_list, OST[fig], color='red', marker='*', linestyle='solid', label='OST')
        plt.plot(handover_list, OTL[fig], color='green', marker='o', linestyle='solid', label='OTL')
        plt.plot(handover_list, PO[fig], color='blue', marker='^', linestyle='solid', label='PO with w=0.5')
        plt.plot(handover_list, APO[fig], color='olive', marker='x', linestyle='solid', label='APO')
        plt.xlabel('Handover frequency', fontsize='x-large')
        plt.ylabel(ylabel_map[fig], fontsize='x-large')
        plt.legend()
        plt.show()


def draw_performance_results_request():
    request_list = [x for x in range(10)]
    OST = dict()
    OTL = dict()
    PO = dict()
    APO = dict()

    OST['state'] = []
    OTL['state'] = []
    PO['state'] = []

    OST['load'] = []
    OTL['load'] = []
    PO['load'] = []

    OST['num_func'] = []
    OTL['num_func'] = []
    PO['num_func'] = []

    for u in request_list:
        filename = "data/pareto_" + 'u' + "_" + str(u) + ".js"
        f = open(filename)
        pareto_optimal_points = ujson.load(f)
        pareto_optimal_points.sort(key=lambda x: x[0])

        OST['state'].append(pareto_optimal_points[0][0])
        OST['load'].append(pareto_optimal_points[0][1])
        OST['num_func'].append(pareto_optimal_points[0][2])

        OTL['state'].append(pareto_optimal_points[len(pareto_optimal_points)-1][0])
        OTL['load'].append(pareto_optimal_points[len(pareto_optimal_points)-1][1])
        OTL['num_func'].append(pareto_optimal_points[len(pareto_optimal_points)-1][2])

        filename = "data/pareto_weight_" + 'u' + "_" + str(u) + ".js"
        f = open(filename)
        pareto_optimal_weight_map = ujson.load(f)
        for point in pareto_optimal_weight_map.keys():
            if 0.5 in pareto_optimal_weight_map[point]:
                p_ = literal_eval(point)
                PO['state'].append(p_[0])
                PO['load'].append(p_[1])
                PO['num_func'].append(p_[2])
                break

        print('--------------------------', u, '-----------')
        print('best state', pareto_optimal_points[0][0])
        print('worst state', pareto_optimal_points[len(pareto_optimal_points)-1][0])
        print('best load', pareto_optimal_points[len(pareto_optimal_points)-1][1])
        print('worst load', pareto_optimal_points[0][1])
        print('PO state', p_[0])
        print('PO load', p_[1])

        APO['state'] = [2500.0, 2500.0, 2500.0, 2500.0, 2500.0, 3200.0, 3600.0, 3600.0, 3600.0, 3600.0]
        APO['load'] = [27500.0, 55000.0, 82500.0,110000.0, 137500.0, 132000.0, 115500.0, 132000.0, 148500, 165000.0]
        APO['num_func'] = [2.0, 2.0, 2.0, 2.0, 2.0,3.0, 4.0, 4.0, 4.0, 4.0]
    figures = ['state', 'load', 'num_func']
    ylabel_map = {'state': 'State Transfer Cost', 'load': 'Traffic Load', 'num_func': 'Number of StateMF sets'}
    for fig in figures:
        plt.plot(request_list, OST[fig], color='red', marker='*', linestyle='solid', label='OST')
        plt.plot(request_list, OTL[fig], color='green', marker='o', linestyle='solid', label='OTL')
        plt.plot(request_list, PO[fig], color='blue', marker='^', linestyle='solid', label='PO with w=0.5')
        plt.plot(request_list, APO[fig], color='olive', marker='x', linestyle='solid', label='APO')
        plt.xlabel('Number of session requests', fontsize='x-large')
        plt.ylabel(ylabel_map[fig], fontsize='x-large')
        plt.legend()
        plt.show()


def draw_performance_results_ue():
    ue_num_list = [1] + [50*x for x in range(20) if x != 0]
    OST = dict()
    OTL = dict()
    PO = dict()
    APO = dict()

    OST['state'] = []
    OTL['state'] = []
    PO['state'] = []

    OST['load'] = []
    OTL['load'] = []
    PO['load'] = []

    OST['num_func'] = []
    OTL['num_func'] = []
    PO['num_func'] = []

    for n in ue_num_list:
        filename = "data/pareto_" + 'n' + "_" + str(n) + ".js"
        f = open(filename)
        pareto_optimal_points = ujson.load(f)
        pareto_optimal_points.sort(key=lambda x: x[0])

        OST['state'].append(pareto_optimal_points[0][0])
        OST['load'].append(pareto_optimal_points[0][1])
        OST['num_func'].append(pareto_optimal_points[0][2])

        OTL['state'].append(pareto_optimal_points[len(pareto_optimal_points)-1][0])
        OTL['load'].append(pareto_optimal_points[len(pareto_optimal_points)-1][1])
        OTL['num_func'].append(pareto_optimal_points[len(pareto_optimal_points)-1][2])

        filename = "data/pareto_weight_" + 'n' + "_" + str(n) + ".js"
        f = open(filename)
        pareto_optimal_weight_map = ujson.load(f)
        for point in pareto_optimal_weight_map.keys():
            if 0.5 in pareto_optimal_weight_map[point]:
                p_ = literal_eval(point)
                PO['state'].append(p_[0])
                PO['load'].append(p_[1])
                PO['num_func'].append(p_[2])
                break

        print('--------------------------', n, '-----------')
        print('best state', pareto_optimal_points[0][0])
        print('worst state', pareto_optimal_points[len(pareto_optimal_points)-1][0])
        print('best load', pareto_optimal_points[len(pareto_optimal_points)-1][1])
        print('worst load', pareto_optimal_points[0][1])
        print('PO state', p_[0])
        print('PO load', p_[1])

        APO['state'] = [2500.0, 2500.0, 2500.0, 2500.0, 2500.0, 2500.0, 2500.0, 2500.0, 2500.0, 2500.0, 3200.0, 3200.0,
                        3600.0, 3200.0, 3600.0, 3600.0, 3600.0, 3600.0, 3600.0, 3600.0]
        APO['load'] = [300.0, 15000.0, 30000.0, 45000.0, 60000.0, 75000.0, 90000.0, 105000.0, 120000.0, 135000.0,
                       120000.0, 132000.0, 108000, 156000, 126000.0, 135000.0, 144000.0, 153000.0, 162000.0, 171000.0]
        APO['num_func'] = [2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 3.0, 3.0, 4.0, 3.0, 4.0, 4.0, 4.0, 4.0,
                           4.0, 4.0]
    figures = ['state', 'load', 'num_func']
    ylabel_map = {'state': 'State Transfer Cost', 'load': 'Traffic Load', 'num_func': 'Number of StateMF sets'}
    for fig in figures:
        plt.plot(ue_num_list, OST[fig], color='red', marker='*', linestyle='solid', label='OST')
        plt.plot(ue_num_list, OTL[fig], color='green', marker='o', linestyle='solid', label='OTL')
        plt.plot(ue_num_list, PO[fig], color='blue', marker='^', linestyle='solid', label='PO with w=0.5')
        plt.plot(ue_num_list, APO[fig], color='olive', marker='x', linestyle='solid', label='APO')
        plt.xlabel('Number of UEs', fontsize='x-large')
        plt.ylabel(ylabel_map[fig], fontsize='x-large')
        plt.legend()
        plt.show()


draw_running_time()