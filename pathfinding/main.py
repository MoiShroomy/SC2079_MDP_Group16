from world_execute_me.map import Map
from 縁結び.dubins import Dubins
from 縁結び.reeds_shepp import RS

d = Dubins(20)
r = RS()
m = Map([])
print(m.generate_edges([(0,0,0), (40, 70, 0)], r))