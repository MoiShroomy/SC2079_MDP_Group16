from world_execute_me.map import Map
from world_execute_me.obstacle import Obstacle
from 縁結び.dubins import Dubins
from 縁結び.reeds_shepp import RS

d = Dubins(20)
r = RS()
obstacles = [Obstacle(40, 70, 0)]
m = Map(obstacles)
#print(m.generate_edges([(0,0,0), (40, 70, 0)], r))
m.generate_goals(obstacles)