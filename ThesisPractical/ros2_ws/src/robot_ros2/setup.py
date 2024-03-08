import os
from glob import glob
from setuptools import setup

package_name = 'hospital_carrier'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
        ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch')),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
        (os.path.join('share', package_name, 'config'), glob('config/*.yaml')),
        (os.path.join('share', package_name, 'urdf'), glob('urdf/*.xacro')),
        (os.path.join('share', package_name, 'meshes'), glob('meshes/*.dae')),
        (os.path.join('share', package_name, 'models'), glob('models/*')),
        (os.path.join('share', package_name, 'data'), glob('data/*')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Name',
    maintainer_email='your@email.com',
    description='Onboard software for robot carrier',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            "EncoderSim = hospital_carrier.EncoderSim:main",
            "OdomCalculator = hospital_carrier.OdomCalculator:main",
            "Follower = hospital_carrier.Follower:main",
            "Localizer = hospital_carrier.Localizer:main",
            "Odrives = hospital_carrier.Odrives:main",
            "OperationModeControl = hospital_carrier.OperationModeControl:main",
            "PS4Controller = hospital_carrier.PS4Controller:main",
            "CoordinateNavigator = hospital_carrier.CoordinateNavigator:main",
            "DebugDisplay = hospital_carrier.DebugDisplay:main",
            "ReadAruco = hospital_carrier.ReadAruco:main",
            "MqttListener = hospital_carrier.MqttListener:main",
            "MqttRemoteControl = hospital_carrier.MqttRemoteControl:main",
            "MqttVideoStreamer = hospital_carrier.MqttVideoStreamer:main",
            "MqttOdomAndStatus = hospital_carrier.MqttOdomAndStatus:main",
            "PointcloudToPly = hospital_carrier.PointcloudToPly:main"
        ],
    },
)