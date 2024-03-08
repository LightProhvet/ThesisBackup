from setuptools import find_packages
from setuptools import setup

setup(
    name='robot_ros2_msgs',
    version='0.0.0',
    packages=find_packages(
        include=('robot_ros2_msgs', 'robot_ros2_msgs.*')),
)
