import asyncio
import logging
import random
import argparse
from viam.robot.client import RobotClient
from viam.rpc.dial import Credentials, DialOptions
from viam.components.gantry import Gantry

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

async def main():
    robot = await connect()
    logger = logging.getLogger("axidraw")
    
    axidraw = Gantry.from_robot(robot, "axidraw")
    axis = await axidraw.get_lengths()
    start = await axidraw.get_position()
    
    # make sure its at the origin
    await axidraw.move_to_position([0, 0, 0], [])

    # Don't forget to close the robot when you're done!
    await robot.close()

if __name__ == "__main__":
    asyncio.run(main())