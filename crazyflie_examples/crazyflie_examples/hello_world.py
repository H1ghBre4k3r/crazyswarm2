# from crazyflie_py import Crazyswarm
# from crazyflie_py.crazyflie import Crazyflie, CrazyflieServer
# from crazyflie_py.uav_trajectory import Trajectory, Polynomial4D
# from rclpy import logging
# import numpy as np
# import math
# from pathlib import Path


# TAKEOFF_DURATION = 2.5
# HOVER_DURATION = 5.0
# MOVE_DURATION = 2.0

# height = 2.0
# center = np.array([0.0, 0.0, height])
# r = 1.0

# logger = logging.get_logger("TEST")


# def position(x=0, y=0, z=height):
#     return np.array([x, y, z])


# def direction(x=0, y=0, z=0):
#     return np.array([x, y, z])

# # def main():
# #     swarm = Crazyswarm()
# #     timeHelper = swarm.timeHelper
# #     cfs = swarm.allcfs

# #     cfs.takeoff(targetHeight=height, duration=1.0)
# #     timeHelper.sleep(TAKEOFF_DURATION)

# #     circle = [position(1, 0), position(0, 1), position(-1, 0), position(0, -1)]

# #     for i in range(3600):
# #         flies: list[Crazyflie] = cfs.crazyflies

# #         for j in range(len(flies)):
# #             cf = flies[j]
# #             cf.goTo(circle[(i + j) % 4], yaw=0, duration=MOVE_DURATION);

# #         timeHelper.sleep(MOVE_DURATION)

# #     timeHelper.sleep(TAKEOFF_DURATION + HOVER_DURATION)


# class MyTrajectory(Trajectory):
#     def __init__(self):
#         super().__init__()
#         self.data = []

#     def fly_to(self, x, y, z, duration):
#         new_data = [0.0] * 33
#         new_data[0] = float(duration)
#         new_data[2] = float(x)
#         new_data[10] = float(y)
#         new_data[18] = float(z)
#         self.data.append(new_data)

#     def compile(self):
#         data = np.array(self.data)
#         self.polynomials = [Polynomial4D(row[0], row[1:9],
#                                          row[9:17], row[17:25], row[25:33]) for row in data]
#         self.duration = np.sum(data[:, 0])


# def circle(traj: MyTrajectory):
#     DURATION = 0.5

#     traj.fly_to(1, 0, 0, DURATION)
#     traj.fly_to(0.75, 0.75, 0, DURATION)
#     traj.fly_to(0, 1, 0, DURATION)
#     traj.fly_to(-0.75, 0.75, 0, DURATION)
#     traj.fly_to(-1, 0, 0, DURATION)
#     traj.fly_to(-0.75, -0.75, 0, DURATION)
#     traj.fly_to(0, -1, 0, DURATION)
#     traj.fly_to(0.75, -0.75, 0, DURATION)


# def main():
#     swarm = Crazyswarm()
#     timeHelper = swarm.timeHelper
#     allcfs = swarm.allcfs

#     traj1 = MyTrajectory()
#     circle(traj1)
#     circle(traj1)
#     circle(traj1)
#     circle(traj1)

#     traj1.compile()

#     print(f"{traj1}")

#     # enable logging
#     allcfs.setParam('usd.logging', 1)

#     TRIALS = 1
#     TIMESCALE = 1.0
#     for _ in range(TRIALS):

#         flies: list[Crazyflie] = allcfs.crazyflies

#         for cf in flies:
#             cf.uploadTrajectory(0, 0, traj1)

#         allcfs.takeoff(targetHeight=1.0, duration=2.0)
#         timeHelper.sleep(2.5)
#         for cf in flies:
#             pos = np.array(cf.initialPosition) + np.array([0, 0, 1.0])
#             cf.goTo(pos, 0, 2.0)
#         timeHelper.sleep(2.5)

#         for i, cf in enumerate(flies):
#             cf.startTrajectory(0, timescale=TIMESCALE)

#         timeHelper.sleep(traj1.duration * TIMESCALE + 2.0)
#         # allcfs.startTrajectory(0, timescale=TIMESCALE, reverse=True)
#         # timeHelper.sleep(traj1.duration * TIMESCALE + 2.0)

#         allcfs.land(targetHeight=0.06, duration=2.0)
#         timeHelper.sleep(3.0)

#     # disable logging
#     allcfs.setParam('usd.logging', 0)


# if __name__ == '__main__':
#     main()
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

# LEFT_CENTER = np.array([R, R, Z])

# RIGHT_CENTER = LEFT_CENTER + np.array([R, 0, 0])

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

POSITIONS = [
    left(R, 0, 0),
    right(R, 0, 0),
    left(-R, 0, 0),
    right(-R, 0, 0),
    left(0, R, 0),
    right(0, 0, R),
    left(0, -R, 0),
    right(0, 0, -R),
]

def main():
    swarm = Crazyswarm()
    timeHelper = swarm.timeHelper
    allcfs = swarm.allcfs
    flies: list[Crazyflie] = allcfs.crazyflies

    # traj1 = Trajectory()
    # traj1.loadcsv('/root/ros2_ws/src/crazyswarm2/crazyflie_examples/crazyflie_examples/data/circle.csv')

    # enable logging
    allcfs.setParam('usd.logging', 1)

    TRIALS = 1
    TIMESCALE = 1.0
    for i in range(TRIALS):

        allcfs.takeoff(targetHeight=Z, duration=5.0)
        timeHelper.sleep(6.0)

        # for f in flies: 
        #     f.takeoff(targetHeight=Z, duration=5.0)
        #     timeHelper.sleep(5.0)

        for (j, cf) in enumerate(flies):
            traj = Trajectory()
            traj.loadcsv(f'/home/louis/ros2_ws/src/crazyswarm2/crazyflie_examples/crazyflie_examples/data/traj{j}.csv')
            cf.uploadTrajectory(0, 0, traj)

        for i, cf in enumerate(flies):
            # pos = np.array(cf.initialPosition) + np.array([0, 0, Z])
            pos = POSITIONS[i]
            cf.goTo(pos, 0, 10.0)
        timeHelper.sleep(10)

        allcfs.startTrajectory(0, timescale=TIMESCALE)
        timeHelper.sleep(4 * 8.0 + 2.0)
        # # allcfs.startTrajectory(0, timescale=TIMESCALE, reverse=True)
        # # timeHelper.sleep(traj1.duration * TIMESCALE + 2.0)

        for cf in flies:
            pos = np.array(cf.initialPosition) + np.array([0, 0, Z])
            cf.goTo(pos, 0, 4.0)
        timeHelper.sleep(5.0)

        for f in flies:
            f.land(targetHeight=0.10, duration=5.0)
            timeHelper.sleep(5.0)

        # allcfs.land(targetHeight=0.10, duration=5.0)
        # timeHelper.sleep(5.0)

    # disable logging
    allcfs.setParam('usd.logging', 0)


if __name__ == '__main__':
    main()
