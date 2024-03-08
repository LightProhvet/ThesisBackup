import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'semantic_segmentation'

setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        # ('lib/' + package_name, ['semantic_segmentation/models/__init__.py']),
        # ('lib/' + package_name + '/models', glob('models/*')),
    ],
    install_requires=[
        'setuptools',
        'numpy',
        'tensorflow',
    ],
    zip_safe=True,
    #   <maintainer email="dheera@dheera.net">dheera</maintainer>
    maintainer='dheera',
    maintainer_email='dheera@dheera.net',
    description='Semantic segmentation',
    license='BSD',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'segmentation = semantic_segmentation.segmentation_node:main',
        ],
    },
)
