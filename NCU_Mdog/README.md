# ncu_mdog

## About The Project
This is the drivers and sample code of ncu_mdog.
<p align="right">(<a href="#top">back to top</a>)</p>

### Hardware List

+ jetson nano 4GB
+ Ydlidar X4
+ Intel Realsence D435i
+ MPU9250
+ HTS-20L * 12
+ [One-Wire Serial Bus Servo Controller Board](https://www.hiwonder.com/products/serial-bus-servo-controller)


### Built With

+ jetson nano 4GB
+ Ubuntu 18.04
+ ROS 2
+ [RTIMULIB](https://github.com/jetsonhacks/RTIMULib)

<p align="right">(<a href="#top">back to top</a>)</p>

## Getting Started
### Prerequisites
+ apt part
 ```sh
sudo apt updat
sudo apt-get install build-essential python3-colcon-common-extensions python3-rosdep
```
+ cmake part
 ```sh
cd ~
git clone https://github.com/jetsonhacks/RTIMULib.git

cd RTIMULib/Linux
mkdir build
cd build
cmake .. -DBUILD_DEMO=0 -DBUILD_GL=0
make -j4
sudo make install
sudo ldconfig
```

+ python package
```sh
pip install pyserial
```

### Installation

Place the package in a ROS 2 workspace's `src` directory and build it with its
workspace dependencies:
```sh
cd ~/ros2_ws
rosdep install --from-paths src --ignore-src -r -y
colcon build --packages-select ncu_mdog
source install/setup.bash
cd "$(ros2 pkg prefix ncu_mdog)/share/ncu_mdog/startup"
sudo chmod 777 ./*
sudo sh initenv.sh
```
<p align="right">(<a href="#top">back to top</a>)</p>

## Usage

```sh
ros2 launch ncu_mdog project_sample.launch.py
```

The RealSense launch is optional and can be enabled with
`launch_realsense:=true` when a ROS 2 `realsense2_camera` package is installed.

## Acknowledgments

+ [RTIMULIB](https://github.com/jetsonhacks/RTIMULib.git)

<p align="right">(<a href="#top">back to top</a>)</p>

