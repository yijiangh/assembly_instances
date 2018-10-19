For the new URDF files, we use [xacro]() initially to compile URDFs, which requires a ROS catkin system. But most of the URDFs should be compiled and ready-to-go.

## Usage

- Step 1: create a catkin workspace, see [tutorial](http://wiki.ros.org/catkin/Tutorials/create_a_workspace)

- Step 2: cd into the `urdf` folder, and run: `rosrun xacro xacro --inorder -o <file_name>.urdf <file_name>.xacro`

- Step 3 (optional): copy the `` from the `utils` folder to your urdf folder, and run `./xacro2dae.sh <file_name without file suffix>` to generate a dae file (do a `chmod a+x xacro2dae.sh` if needed). Then you can use openrave to visulize it as a quick check: `openrave <file_name>.dae`.
