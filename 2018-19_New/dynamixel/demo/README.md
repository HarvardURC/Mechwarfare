# Demo of Using Dynamixel DX-117 Servo Motors

## Electrical Components
* 3 [DX-117 Servos][DX117 e-Manual]
* [USB2Dynamixel][USB2Dynamixel e-Manual]: A USB to Dynamixel Adapter
* [Dynamixel Power Hub][Power Hub Product Page]
* Power Adapter: 12V~18.5V (Recommended: 14.8V)

## Requirements
* [Dynamixel SDK][SDK Link] needs to be installed before usage.
    * Create a python virtual environment: `virtualenv venv --python=python3`
    * Activate the virtual env: `source venv/bin/activate`
    * Git clone the above SDK github repo in some location
    * `cd` into its `python` directory
    * `python setup.py install`

* Dynamixel servos need to have their IDs set
    * Download Dynamixel's [RoboPlus 1.0][RoboPlus Link] (didn't try 2.0, might also work)
    * Set the IDs of the servos using its Dynamixel Wizard tool

## Run the demo
### Steps:
1. Connect the **servos** to **Power Hub** (either daisy-chained or separate)
2. Connect **USB2Dynamixel** one end to **Power Hub**, and another end to a computer's **USB Port**
3. Connect the **Power Adapter** to **Power Hub**
4. Activate the python **virtual env** that has **Dynamixel SDK** installed
5. `python single_servo.py` or `python multiple_servo.py`

[//]: # (Links referenced in the document are below)
[DX117 e-Manual]: http://support.robotis.com/en/product/actuator/dynamixel/dx_series/dx-117.htm
[USB2Dynamixel e-Manual]: http://support.robotis.com/en/product/auxdevice/interface/usb2dxl_manual.htm
[Power Hub Product Page]: https://www.trossenrobotics.com/6-port-rx-power-hub
[SDK Link]: https://github.com/ROBOTIS-GIT/DynamixelSDK
[RoboPlus Link]: http://www.robotis.us/roboplus1/