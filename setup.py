from setuptools import setup, find_packages

package_name = 'mission_control_gui'

setup(
    name=package_name,
    version='0.0.1',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]) if False else
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='cherry',
    maintainer_email='you@example.com',
    description='PyQt5 GUI for dispatching Nav2 waypoints',
    license='Apache-2.0',
    entry_points={
        'console_scripts': [
            'mission_control_gui = mission_control_gui.main:main',
        ],
    },
)
