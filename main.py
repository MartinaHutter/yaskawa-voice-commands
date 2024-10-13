import configuration as config  
import torch # Import pyTorch for Transformer
import ycom

from voice_command_handler import VoiceCommandHandler  
from test_sentence_speech2 import TestSentenceSpeech 
from robot_control import RobotControl
from ycom import (
    controllers, CartesianLocation, CartesianRotation, CartesianRobotPositionRobot, ControllerClient, 
    ProtocolType, PulseRobotPosition
)

print("setting up the controller")
# Constructs the controller client for the controller "YRC1000" available at host address
# "192.168.0.100" using the High-speed Ethernet Protocol (HEP).
controller_client = ControllerClient.construct(
    controllers.YRC1000, "192.168.0.1", ProtocolType.HEP
)

# Sets the controller parameter RS022 (Permission of instance 0) of the controller client according
# to the value of the controller to correctly address variables and registers.
# - False : Variable numbers and register numbers start from 1.
# - True  : Variable numbers and register numbers start from 0.
controller_client.parameter_rs022 = True

# Gets the robot count, supported by the controller (8 for YRC1000).
robot_count = controller_client.controller.robot_count

# Gets the station count, supported by the controller (24 for YRC1000).
station_count = controller_client.controller.station_count

# Gets the I/O group count for the network output domain.
network_output_count = controller_client.controller.io_domain_network_output.group_count
print(network_output_count)

# Turn on robot servos.
controller_client.servos_turn(True)


def main():
    robot_controller = RobotControl(controller_client)
    voice_handler = VoiceCommandHandler(controller_client)
    new_sentence_processor = TestSentenceSpeech(controller_client)  # Instantiate the class

    while True:
        # Wait for activation sound
        if voice_handler.waiting_for_activation_command(config.ACTIVATION_KEYWORD):
            # Obtain recognized and classified voice command
            for _ in range(config.INVALID_COMMAND_ATTEMPTS):
                command = new_sentence_processor.process_voice_command()  # Get the classified label
                if command:
                    command_lower = command.lower()  # Normalize
                    match command_lower:
                        case _ if "home" in command_lower:
                            robot_controller.home()
                            print("At home position")
                            break
                        case _ if "pick" in command_lower:
                            robot_controller.pick()
                            print("Product picked")
                            break
                        case _ if "place" in command_lower:
                            robot_controller.place()
                            print("Product placed")
                            break
                        case _:
                            print("Unknown command")
                else:
                    break  # Exit if no valid command is recognized

if __name__ == "__main__":
    main()

