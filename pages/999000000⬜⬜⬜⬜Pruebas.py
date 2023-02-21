
import streamlit as st
import matplotlib.pyplot as plt

import pandapower as pp

net = pp.create_empty_network()

pp.create_bus(net, name = "110 kV bar", vn_kv = 110, type = 'b')
pp.create_bus(net, name = "20 kV bar", vn_kv = 20, type = 'b')
pp.create_bus(net, name = "bus 2", vn_kv = 20, type = 'b')
pp.create_bus(net, name = "bus 3", vn_kv = 20, type = 'b')
pp.create_bus(net, name = "bus 4", vn_kv = 20, type = 'b')
pp.create_bus(net, name = "bus 5", vn_kv = 20, type = 'b')
pp.create_bus(net, name = "bus 6", vn_kv = 20, type = 'b')

pp.create_ext_grid(net, 0, vm_pu = 1)

pp.create_line(net, name = "line 0", from_bus = 1, to_bus = 2, length_km = 1, std_type = "NAYY 4x150 SE")
pp.create_line(net, name = "line 1", from_bus = 2, to_bus = 3, length_km = 1, std_type = "NAYY 4x150 SE")
pp.create_line(net, name = "line 2", from_bus = 3, to_bus = 4, length_km = 1, std_type = "NAYY 4x150 SE")
pp.create_line(net, name = "line 3", from_bus = 4, to_bus = 5, length_km = 1, std_type = "NAYY 4x150 SE")
pp.create_line(net, name = "line 4", from_bus = 5, to_bus = 6, length_km = 1, std_type = "NAYY 4x150 SE")
pp.create_line(net, name = "line 5", from_bus = 6, to_bus = 1, length_km = 1, std_type = "NAYY 4x150 SE")

pp.create_transformer_from_parameters(net, hv_bus=0, lv_bus=1, i0_percent=0.038, pfe_kw=11.6,
        vkr_percent=0.322, sn_mva=40, vn_lv_kv=22.0, vn_hv_kv=110.0, vk_percent=17.8)

pp.create_load(net, 2, p_mw = 1, q_mvar = 0.2, name = "load 0")
pp.create_load(net, 3, p_mw = 1, q_mvar = 0.2, name = "load 1")
pp.create_load(net, 4, p_mw = 1, q_mvar = 0.2, name = "load 2")
pp.create_load(net, 5, p_mw = 1, q_mvar = 0.2, name = "load 3")
pp.create_load(net, 6, p_mw = 1, q_mvar = 0.2, name = "load 4")

pp.create_switch(net, bus = 1, element = 0, et = 'l')
pp.create_switch(net, bus = 2, element = 0, et = 'l')
pp.create_switch(net, bus = 2, element = 1, et = 'l')
pp.create_switch(net, bus = 3, element = 1, et = 'l')
pp.create_switch(net, bus = 3, element = 2, et = 'l')
pp.create_switch(net, bus = 4, element = 2, et = 'l')
pp.create_switch(net, bus = 4, element = 3, et = 'l', closed = 0)
pp.create_switch(net, bus = 5, element = 3, et = 'l')
pp.create_switch(net, bus = 5, element = 4, et = 'l')
pp.create_switch(net, bus = 6, element = 4, et = 'l')
pp.create_switch(net, bus = 6, element = 5, et = 'l')
pp.create_switch(net, bus = 1, element = 5, et = 'l')


import pandapower.topology as top
import networkx as nx

mg = top.create_nxgraph(net)
nx.shortest_path(mg, 0, 5)
st.write('vivo')



net.switch.closed.at[11] = 0
top.unsupplied_buses(net)

pp.topology.create_nxgraph(net, respect_switches = False)

# plt.show()