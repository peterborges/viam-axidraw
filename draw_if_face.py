import asyncio
import logging
import random
import argparse
from viam.robot.client import RobotClient
from viam.rpc.dial import Credentials, DialOptions
from viam.components.gantry import Gantry
import numpy as np
from viam.services.vision import VisionClient
from viam.components.camera import Camera
async def connect():
    creds = Credentials(
        type='robot-location-secret',
        payload='yzl1w4e70v5c3pl44nuv9on4r7s6vaug56x3qnm32eqbqd5i')
    opts = RobotClient.Options(
        refresh_interval=0,
        dial_options=DialOptions(credentials=creds)
    )
    return await RobotClient.at_address('mbp-main.8fc0qlpm4c.viam.cloud', opts)

def getValue(minVal: float, maxVal: float) -> float:
    return float(minVal + (maxVal - minVal) * random.random())


def mm2inch(l):
    return l*0.0393701

async def draw_line(axidraw: Gantry, x1, y1, x2, y2):

    pos = await axidraw.get_position()
    #lift the pen
    await axidraw.move_to_position([pos[0], pos[1], 1], [])

    # go to initial point
    await axidraw.move_to_position([x1, y1, 1], [])

    #put down the pen
    await axidraw.move_to_position([x1, y1, 0], [])

    #draw the line
    await axidraw.move_to_position([x2, y2, 0], [])
    
    #lift the pen
    await axidraw.move_to_position([x2, y2, 1], [])





async def main():
    robot = await connect()
    logger = logging.getLogger("axidraw")
    camera_name = 'mac-cam'
    cam1 = Camera.from_robot(robot, camera_name)
# Grab Viam's vision service for the detector
    my_detector = VisionClient.from_robot(robot, "detector")
    axidraw = Gantry.from_robot(robot, "axidraw")
    while True:
        detections = await my_detector.get_detections_from_camera(camera_name)

        print(detections)
        if detections[0].confidence>.8:
        # if len(detections) > 1:
            await draw_line(axidraw, 0,0,10,10)
    

    await robot.close()

if __name__ == "__main__":
    asyncio.run(main())



