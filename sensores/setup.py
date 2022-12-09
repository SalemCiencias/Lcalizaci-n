from setuptools import setup

package_name = 'sensores'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='AndreJuan',
    maintainer_email='juan567@ciencias.unam.mx/andrebarra@ciencias.unam.mx',
    description='Paquete para manejar los sensores físicos.',
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'arduino = sensores.arduino:main',
            'probabilidad= sensores.probabilidad:main'
        ],
    },
)
