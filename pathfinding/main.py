from world_execute_me.map import Map
from 縁結び.dubins import Dubins

d = Dubins(20)
m = Map([])
print(m.generate_edges([(0,0,0), (40, 70, 0)], d))