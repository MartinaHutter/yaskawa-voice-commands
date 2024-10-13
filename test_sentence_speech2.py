from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import torch
from voice_command_handler import VoiceCommandHandler

import ycom

from ycom import (
    controllers, CartesianLocation, CartesianRotation, CartesianRobotPositionRobot, ControllerClient, 
    ProtocolType, PulseRobotPosition
)

class TestSentenceSpeech:
    def __init__(self, controller_client):
        # Initialize the voice handler
        self.voice_handler = VoiceCommandHandler(controller_client)

        # Load the fine-tuned model
        self.model = SentenceTransformer('fine-tuned-sentence-transformer/')  # Update with your model path

        # List of training sentences (commands)
        self.sentences = [
            "Pick the object", "Pick the product", "Pick the cube", "Pick the thing", "Lift the thing",
            "Lift the object", "Lift the cube", "Lift it up", "Grab the cube", "Grab the object",
            "Grab the product", "Get the cube", "Get it", "Get the object", "Get the product",
            "Place the object on table", "Place the product on table", "Place the object", "Place it down",
            "Put down the object", "Put it down", "Leave it", "Leave it down", "Move to home position",
            "Go home", "Go to home position", "Parking position"
        ]

        # Corresponding labels for the sentences
        self.labels = [
            "pick", "pick", "pick", "pick", "pick", "pick", "pick", "pick", "pick", 
            "pick", "pick", "pick", "pick", "pick", "pick", "place", "place", "place", "place", 
            "place", "place", "place", "place", "home", "home", "home", "home"
        ]

    def process_voice_command(self):
        # Obtain the voice command from the voice handler
        command = self.voice_handler.get_voice_command()
        if not command:
            return None  # Return None if no command is recognized
        
        # Encode the test sentence using the fine-tuned transformer model
        test_embedding = self.model.encode(command, convert_to_tensor=True)

        max_similarity = -1
        most_similar_sentence = ""
        predicted_label = ""

        # Loop through each sentence and calculate similarity
        for i, sentence in enumerate(self.sentences):
            sentence_embedding = self.model.encode(sentence, convert_to_tensor=True)
            similarity = cosine_similarity(sentence_embedding.cpu().detach().numpy().reshape(1, -1),
                                           test_embedding.cpu().detach().numpy().reshape(1, -1))

            # Update max_similarity and predicted_label if higher similarity is found
            if similarity > max_similarity:
                max_similarity = similarity
                most_similar_sentence = sentence
                predicted_label = self.labels[i]  # Access the label for the most similar sentence

        print(f"Command: {command}, Most similar sentence: '{most_similar_sentence}', Predicted label: {predicted_label}")
        return predicted_label  # Return the label (pick, place, home)

