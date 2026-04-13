from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'smart_robot'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ubuntu',
    maintainer_email='ubuntu@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'ultrasonic_node = smart_robot.ultrasonic_sensor_node:main',
            'motor_decision_node = smart_robot.motor_decision_node:main',
            'motor_node = smart_robot.motor_node:main',
            'decision_node = smart_robot.decision_node:main',
            'control_node = smart_robot.control_node:main',
            'control_client_node = smart_robot.control_client_node:main',
        ],
    },
)
