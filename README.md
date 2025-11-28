# Lab 4

### Steps 1-3
For steps 1-3, you can use the MATLAB or Python starter code provided. First, make your own copy personal copy of the Lab 4 repo with the `Use This Template` button. Then, for MATLAB users, you will need to `git clone` this repository onto your personal computer via: If using Python, you have the option of cloning on your personal machine or on eceprog. If using eceprog, please run the `git clone` command from your home directory.


### Step 4
#### Instructions for all users

For all students, you will need to first edit `ws4/src/msee22_description/urdf/msee22.urdf.xacro` depending on if you use humble or jazzy. Follow the instructions on lines 89 and 95.

Then, build all packages. If you get an error, look for the Lab 4 update thread on Piazza - there might be a solution already posted there to your particular problem.
```bash
cd ~/ece569-fall2025/ws4/
colcon build --symlink-install
source install/setup.bash
```

Now, check if you can view the robot on the table.
```bash
ros2 launch msee22_description view_room.launch.py
```

Next, check if the `py_joint_pub` package is working:
```bash
ros2 launch msee22_description move_robot.launch.py
```


In the `ws4/src/py_joint_pub/py_joint_pub/joint_publisher_csv.py` file, change line 18 to your filename. 
Also, copy and paste your `<username>.csv` file into the `ws4/src/py_joint_pub/py_joint_pub/resource` folder.
Once your have added your csv file to the `resource` folder, build and source your workspace. Then, run 
```bash
ros2 launch msee22_description move_robot.launch.py
```
