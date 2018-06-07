# number of cloud centers, service areas
M_dc = 12
M_sa = 12
dc = ['dc' + str(i) for i in range(M_dc)]
sa = ['sa' + str(i) for i in range(M_sa)]

# traffic amount for signal and session req
L_sig = 10
L_session = 10
Traffic_max = 250000
State_max = 6900

# constants to draw pareto front
ue_num_list = [150, 550, 950]
line_style_map_ue = dict()
line_style_map_ue[150] = {'marker_color': 'blue', 'label': 'UE Num = 150'}
line_style_map_ue[550] = {'marker_color': 'red', 'label': 'UE Num = 550'}
line_style_map_ue[950] = {'marker_color': 'green', 'label': 'UE Num = 950'}

handover_list = [20, 40, 60]
line_style_map_handover = dict()
line_style_map_handover[20] = {'marker_color': 'blue', 'label': 'Handover Freq = 20'}
line_style_map_handover[40] = {'marker_color': 'red', 'label': 'Handover Freq = 40'}
line_style_map_handover[60] = {'marker_color': 'green', 'label': 'Handover Freq = 60'}

ue_num_list = [2, 4, 6]
line_style_map_request = dict()
line_style_map_request[2] = {'marker_color': 'blue', 'label': 'Request num = 2'}
line_style_map_request[4] = {'marker_color': 'red', 'label': 'Request num = 4'}
line_style_map_request[6] = {'marker_color': 'green', 'label': 'Request num = 6'}

annotate_map_request = dict()
annotate_map_request[2] = {(2500.0, 82500.0): 'w=0.5', (1600.0, 132000.0): 'w=0.6', (4000.0, 33000.0): 'w=0.4', (900.0, 148500.0) :'w=1', (4500.0,16500.0):'w=0' }
annotate_map_request[4] = {(2500.0, 137500.0): 'w=0.5', (4000.0, 55000.0): 'w=0.4', (1600.0, 220000.0): 'w=0.6' }
annotate_map_request[6] = {(2500.0, 192500.0): 'w=0.5', (4000.0, 77000.0): 'w=0.4', (3200.0, 154000.0): 'best balance', (4500.0,38500.0):'w=0', (2400.0,231000.0):'w=1'}

annotate_map_handover = dict()
annotate_map_handover[20] = {(1000.0, 165000.0): 'w=0.5', (960.0, 198000.0): 'w=0.8', (1600.0, 66000.0): 'w=0.4', (840.0,231000.0):'w=1', (1800.0,33000.0):'w=0' }
annotate_map_handover[40] = {(2000.0, 165000.0): 'w=0.5', (3200.0, 66000.0): 'w=0.4', (1920.0, 198000.0): 'w=0.8', (2560.0 ,132000.0):'best balance'}
annotate_map_handover[60]= {(3000.0, 165000.0): 'w=0.5', (4800.0, 66000.0): 'w=0.4', (2880.0, 198000.0): '0.8'}

annotate_map_ue = dict()
annotate_map_ue[150] = {(2500.0, 45000.0): 'w=0.5', (1600.0, 72000.0): 'w=0.6', (4000.0, 18000.0): 'w=0.4', (900.0,81000.0):'w=1', (4500.0,9000.0):'w=0' }
annotate_map_ue[550] = {(2500.0, 165000.0): 'w=0.5', (4000.0, 66000.0): 'w=0.4', (2400.0, 198000.0): 'w=0.8', (3200.0,132000.0) :'best balance'}
annotate_map_ue[950] = {(4000.0, 114000.0): 'w=0.5', (3600.0, 171000.0): 'w=0.6'}
