import time
import ycom

from ycom import (
    controllers, CartesianLocation, CartesianRotation, CartesianRobotPositionRobot, ControllerClient, 
    ProtocolType, PulseRobotPosition
)

class RobotControl:
    def __init__(self, controller_client):
        self.controller_client = controller_client

    def home(self):
        
        

        # Constructs a cartesian robot position (in the coordinate system of the robot).
        cartesian_robot_position = CartesianRobotPositionRobot(
            # X-location: 20 millimeters
            location = CartesianLocation(value_x = 560 * 1_000, value_y = 0 * 1_000, value_z = 484 * 1_000),
            # Z-rotation: 90 degrees
            rotation = CartesianRotation(value_x = -164 * 10_000, value_y = -89 * 10_000, value_z = -15 * 10_000)
        )
        
        # Moves the robot to a cartesian position using a linear movement with a speed of
        # 100 millimeters per second.
        self.controller_client.robot_move_linear_cartesian(0, cartesian_robot_position, 100 * 10)

        
        


    def pick(self):
        
        # Check if gripper is empty, if empty, B021 = 0 else 64
        # Gets the value of the first byte variable.
        byte = self.controller_client.variable_byte_value_get(20)
        #print(byte)

        # Check if byte is true, if the robot gripper is empty
        if (byte != 64):  # This will execute if byte is True

            # Move the robot to pre-pick position (above the object)
            # Constructs a cartesian robot position (in the coordinate system of the robot).
            cartesian_robot_position = CartesianRobotPositionRobot(
                # X-location: 20 millimeters
                location = CartesianLocation(value_x = 460 * 1_000, value_y = -303 * 1_000, value_z = -157 * 1_000),
                # Z-rotation: 90 degrees
                rotation = CartesianRotation(value_x = 179 * 10_000, value_y = -1 * 10_000, value_z = 22 * 10_000)
            )
        
            # Moves the robot to a cartesian position using a linear movement with a speed of
            # 100 millimeters per second.
            self.controller_client.robot_move_linear_cartesian(0, cartesian_robot_position, 100 * 10)



            # Now move the robot to the pick position (vacuum gripper is touching the product)
            # This time, robot will move in linear motion and in robot coordinates
            # Constructs a cartesian robot position (in the coordinate system of the robot).
            cartesian_robot_position = CartesianRobotPositionRobot(
                # X-location: 20 millimeters
                location = CartesianLocation(value_x = 460 * 1_000, value_y = -303 * 1_000, value_z = -249 * 1_000),
                # Z-rotation: 90 degrees
                rotation = CartesianRotation(value_x = 179 * 10_000, value_y = -1 * 10_000, value_z = 22 * 10_000)
            )
        
            # Moves the robot to a cartesian position using a linear movement with a speed of
            # 100 millimeters per second.
            self.controller_client.robot_move_linear_cartesian(0, cartesian_robot_position, 100 * 10)
        
            # Turn on the vacuum gripper
            # Sets the value of the first network input group (I/O group number 2,701 for YRC1000).
            #controller_client.io_group_value_set(2_701, 0x44)

            # Selects a job for execution. This job turns on the output OUT18 in IO307 to turn on the gripper (ycom can access IOs after they are mapped in ladder)
            self.controller_client.job_select_execution("GET_PART")
            # Adjustment to the ambient noise
            # Start the job selected for execution and waits while the job is running.
            self.controller_client.job_start_and_wait()
            time.sleep(4) # timer to make sure that gripper closes fully (vacuum soft gripper)

            # Lift the object with a linear motion
            # Constructs a cartesian robot position (in the coordinate system of the robot).
            cartesian_robot_position = CartesianRobotPositionRobot(
                # X-location: 20 millimeters
                location = CartesianLocation(value_x = 460 * 1_000, value_y = -303 * 1_000, value_z = -157 * 1_000),
                # Z-rotation: 90 degrees
                rotation = CartesianRotation(value_x = 179 * 10_000, value_y = -1 * 10_000, value_z = 22 * 10_000)
            )
        
            # Moves the robot to a cartesian position using a linear movement with a speed of
            # 100 millimeters per second.
            self.controller_client.robot_move_linear_cartesian(0, cartesian_robot_position, 100 * 10)

            # Set variable, that object was picked
            # Sets the value of the first byte variable.
            self.controller_client.variable_byte_value_set(20, 0x40)

            # Move away into the middle position after the object is picked with a linear motion
            # Constructs a cartesian robot position (in the coordinate system of the robot).
            cartesian_robot_position = CartesianRobotPositionRobot(
                # X-location: 20 millimeters
                location = CartesianLocation(value_x = 460 * 1_000, value_y = -18 * 1_000, value_z = 69 * 1_000),
                # Z-rotation: 90 degrees
                rotation = CartesianRotation(value_x = 179 * 10_000, value_y = -1 * 10_000, value_z = 22 * 10_000)
            )
        
            # Moves the robot to a cartesian position using a linear movement with a speed of
            # 100 millimeters per second.
            self.controller_client.robot_move_linear_cartesian(0, cartesian_robot_position, 100 * 10)

        else:
            print("Execution terminated: gripper is full, I cannot pick")

    def place(self):
        
        # Check, if the robot is holding the object
        # Gets the value of the first byte variable.
        byte = self.controller_client.variable_byte_value_get(20)
        #print(byte)

        # Check if byte is true, if the robot is holding the object
        if (byte == 64):  # This will execute if byte is True
            # Move the robot to pre-place position
            # Constructs a cartesian robot position (in the coordinate system of the robot).
            cartesian_robot_position = CartesianRobotPositionRobot(
                # X-location: 20 millimeters
                location = CartesianLocation(value_x = 546 * 1_000, value_y = 168 * 1_000, value_z = -159 * 1_000),
                # Z-rotation: 90 degrees
                rotation = CartesianRotation(value_x = 179 * 10_000, value_y = -1 * 10_000, value_z = 22 * 10_000)
            )
        
            # Moves the robot to a cartesian position using a linear movement with a speed of
            # 100 millimeters per second.
            self.controller_client.robot_move_linear_cartesian(0, cartesian_robot_position, 100 * 10)

            
            # Move the robot to the place position (object is touching the table)
            # Constructs a cartesian robot position (in the coordinate system of the robot).
            cartesian_robot_position = CartesianRobotPositionRobot(
                # X-location: 20 millimeters
                location = CartesianLocation(value_x = 546 * 1_000, value_y = 168 * 1_000, value_z = -253 * 1_000),
                # Z-rotation: 90 degrees
                rotation = CartesianRotation(value_x = 179 * 10_000, value_y = -1 * 10_000, value_z = 22 * 10_000)
            )
        
            # Moves the robot to a cartesian position using a linear movement with a speed of
            # 100 millimeters per second.
            self.controller_client.robot_move_linear_cartesian(0, cartesian_robot_position, 100 * 10)
        

            # Turn off the vacuum gripper
            # Sets the value of the first network input group (I/O group number 2,701 for YRC1000).
            #controller_client.io_group_value_set(2_701, 0x00)

            # Selects a job for execution. This job turns off the output OUT18 in IO307 to turn off the gripper (ycom can access IOs after they are mapped in ladder)
            self.controller_client.job_select_execution("PUT_PART")
            # Start the job selected for execution and waits while the job is running.
            self.controller_client.job_start_and_wait()
            time.sleep(1) # timer to make sure vacuum is off

            # Move from the object with a linear motion
            # Constructs a cartesian robot position (in the coordinate system of the robot).
            cartesian_robot_position = CartesianRobotPositionRobot(
                # X-location: 20 millimeters
                location = CartesianLocation(value_x = 546 * 1_000, value_y = 168 * 1_000, value_z = -159 * 1_000),
                # Z-rotation: 90 degrees
                rotation = CartesianRotation(value_x = 179 * 10_000, value_y = -1 * 10_000, value_z = 22 * 10_000)
            )
        
            # Moves the robot to a cartesian position using a linear movement with a speed of
            # 100 millimeters per second.
            self.controller_client.robot_move_linear_cartesian(0, cartesian_robot_position, 100 * 10)

        
            # Set variable, that object was placed (gripper is empty)
            # Sets the value of the first byte variable.
            self.controller_client.variable_byte_value_set(20, 0x00)

            
        else:
            print("Execution terminated: gripper is empty")


