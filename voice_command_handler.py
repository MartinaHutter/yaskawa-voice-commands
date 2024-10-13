import speech_recognition as sr
import pygame
import configuration as config


import ycom

from ycom import (
    controllers, CartesianLocation, CartesianRotation, CartesianRobotPositionRobot, ControllerClient, 
    ProtocolType, PulseRobotPosition
)


class VoiceCommandHandler:

    def __init__(self, controller_client):
        self.recognizer = sr.Recognizer()
        self.language = config.LANGUAGE
        pygame.mixer.init()
        pygame.mixer.music.load(config.ACTIVATION_SOUND_PATH)
        self.controller_client = controller_client

    def get_voice_command(self):
        with sr.Microphone() as source:
            pygame.mixer.music.play()  # Activation sound
            print("Listening...")
            '''
            # Selects a job for execution.
            self.controller_client.job_select_execution("LISTENING")
            '''
            # Adjustment to the ambient noise
            # Start the job selected for execution and waits while the job is running.
            '''
            self.controller_client.job_start_and_wait()
            '''

            if config.DYNAMIC_MIC_ADJUSTMENT:
                self.recognizer.adjust_for_ambient_noise(source)
            try:
                audio = self.recognizer.listen(source)
                print("Processing...")
                '''
                self.controller_client.job_select_execution("PROCESSING")
                self.controller_client.job_start_and_wait()
                '''
                command = self.recognizer.recognize_google(audio, language=self.language)
                print(f"Command: {command}")  # Recognized command
                return command
            except sr.UnknownValueError:
                print("Try again")
                return None
            except sr.RequestError as e:
                print(f"Error in conversion: {e}")
                return None

    def waiting_for_activation_command(self, activation_keyword=config.ACTIVATION_KEYWORD):
        """
        Waiting for activation sound
        
        Returns True if recognized else False
        """
        print("Waiting for activation...")
        with sr.Microphone() as source:
            # Adjustment to the ambient noise
            if config.DYNAMIC_MIC_ADJUSTMENT:
                self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)
            try:
                text = self.recognizer.recognize_google(audio, language=self.language)
                if activation_keyword.lower() in text.lower():
                    print("Converting speech to text...") 
                    return True
            except sr.UnknownValueError:
                # Ignoring error if not recognized
                pass
            except sr.RequestError as e:
                print(f"Connection error to service: {e}") 
            return False
