#!/usr/bin/env python

from pathlib import Path

from crazyflie_py import Crazyswarm
from crazyflie_py.crazyflie import Crazyflie
from crazyflie_py.uav_trajectory import Trajectory
import numpy as np

Z = 1.5
R = 0.5

def pos(x, y, z): 
    return np.array([float(x), float(y), float(z)])

def offset(x, y, z):
    center = np.array([x, y, z])
    def inner(x, y, z): 
        return center + np.array([x, y, z])

    return inner

left = offset(0, 0, Z)

right = offset(R, 0, Z)
# POSITIONS = [
#     left(R, 0, 0),
#     right(R, 0, 0),
#     left(0, R, 0),
#     right(0, 0, R),
#     left(-R, 0, 0),
#     right(-R, 0, 0),
#     left(0, -R, 0),
#     right(0, 0, -R),
# ]

#       3
#
#   4       2
#
#5              1
#
#   6       8
#
#       7

#
#
#   3       2
#(-.5,.5)  (.5,.5)
#
#
#   4       2
#(-.5,-.5)  (.5,-.5)
#

POSITIONS = [
    left(R, 0, 0),
    right(R, 0, 0),
    left(-R, 0, 0),
    right(-R, 0, 0),
    # left(0, R, 0),
    # right(0, 0, R),
    # left(0, -R, 0),
    # right(0, 0, -R),
]

def main():
    swarm = Crazyswarm()
    timeHelper = swarm.timeHelper
    allcfs = swarm.allcfs
    flies: list[Crazyflie] = allcfs.crazyflies

    # enable logging
    allcfs.setParam('usd.logging', 1)

    TRIALS = 1
    TIMESCALE = 1.0
    for i in range(TRIALS):

        allcfs.takeoff(targetHeight=Z, duration=5.0)
        timeHelper.sleep(6.0)

        D = 1.0
        for f in flies: 
            pos = np.array(f.initialPosition) + np.array([0, 0, Z])
            f.goTo(pos, 0, D)
        timeHelper.sleep(D)

        for (j, cf) in enumerate(flies):
            traj = Trajectory()
            traj.loadcsv(f'/home/louis/ros2_ws/src/crazyswarm2/crazyflie_examples/crazyflie_examples/data/traj{j}.csv')
            cf.uploadTrajectory(0, 0, traj)

        D = 4.0
        for i, f in enumerate(flies):
            pos = POSITIONS[i]
            f.goTo(pos, 0, D)
        timeHelper.sleep(D)

        allcfs.startTrajectory(0, timescale=TIMESCALE)
        timeHelper.sleep(8.0 * 4.0 + 2.0)
        # allcfs.startTrajectory(0, timescale=TIMESCALE, reverse=True)
        # timeHelper.sleep(traj1.duration * TIMESCALE + 2.0)

        for f in flies:
            pos = np.array(f.initialPosition) + np.array([0, 0, Z])
            f.goTo(pos, 0, 4.0)
        timeHelper.sleep(4.0)

        # for f in flies:
        #     f.land(targetHeight=0.10, duration=5.0)
        #     timeHelper.sleep(5.0)

        allcfs.land(targetHeight=0.10, duration=5.0)
        timeHelper.sleep(5.0)

    # disable logging
    allcfs.setParam('usd.logging', 0)


if __name__ == '__main__':
    main()
