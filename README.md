Application offers an easy voice commands interface to YASKAWA robots.

This application is created for [YASKAWA Robots](https://www.yaskawa.eu.com/), specifically for [YRC1000 generation](https://www.yaskawa.eu.com/products/robots/controller/productdetail/product/yrc1000_583) (it can be also used with YRC1000micro, DX200, FS100 and DX100, however on those platforms, it was not tested).
For communication with a robot, it uses Ycom interface. As a speech recognizer, [Google Speech Recognition](https://cloud.google.com/speech-to-text) was used and sentence transformer model [all-MiniML](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2) by Hugging Face was used for clustering or semantic search in sentences spoken to the robot as voice commands.

## HW Architecture
All code runns on laptop or PC connected to the the robot controller YRC1000 via High Speed Ethernet function (needs to be enabled, YASKAWA Europe enables HSE at the initialization). Establish LAN connection (connect to the LAN2 or LAN3 port on the switch inside the robot controller and set up IP address of the controller and laptop). More details are in [this instruction video](https://www.youtube.com/watch?v=k1dJzDm8Ees).

In order to use speech recognizer, laptop must be connected to the internet.

In-built microphone of the laptop can be easily used.

![HW Architecture](/imgs/NLP-HW_architecture.PNG "HW Architecture")

## SW Architecture
This example uses [Google Speech Recognition](https://cloud.google.com/speech-to-text) and sentence transformer model [all-MiniML](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2). Please, follow individual installation instructions.

To give commands to the robot (motion commands or set or get variables), Ycom interface can be used (will be released end of 2024). YMConnect (C++) or MotoCOM (C++) libraries can be used as alternatives, however both are written in C++ language. You can use only the speech recognition without any interface to the robot (modify the code by removing ycom related commands related to ``controller_client`` and robot_control.py).

![SW Architecture](/imgs/NLP-SW_architecture.PNG "SW Architecture")

## Fine-Tuning of the Sentence Transformer
In order to have more focused transformer (and better results of the neural model), fine-tuning of pre-trained transformer is needed. For fine-tuning, additional sentences (here voice commands) shall be used. In this example, sentences related to this tree operations were selected:
* pick
* place
* home position

Sentences for fine-tuning look like this:
```bash
# Prepare your dataset with sentence and corresponding labels
train_examples = [
    InputExample(texts=["Pick the object"], label=0),  # pick = 0
    InputExample(texts=["Pick the product"], label=0),  # pick = 0
    InputExample(texts=["Pick the cube"], label=0),  # pick = 0
    InputExample(texts=["Pick the thing"], label=0),  # pick = 0
    InputExample(texts=["Lift the thing"], label=0),  # lift = 0
    InputExample(texts=["Lift the object"], label=0),  # lift = 0
    InputExample(texts=["Lift the cube"], label=0),  # lift = 0
    InputExample(texts=["Lift it up"], label=0),  # lift = 0
    InputExample(texts=["Grab the cube"], label=0),  # grab = 0
    InputExample(texts=["Grab the object"], label=0),  # grab = 0
    InputExample(texts=["Grab the product"], label=0),  # grab = 0
    InputExample(texts=["Get the cube"], label=0),  # get = 0
    InputExample(texts=["Get it"], label=0),  # get = 0
    InputExample(texts=["Get the object"], label=0),  # get = 0
    InputExample(texts=["Get the product"], label=0),  # get = 0
    InputExample(texts=["Place the object on table"], label=1),  # place = 1
    InputExample(texts=["Place the product on table"], label=1),  # place = 1
    InputExample(texts=["Place the object"], label=1),  # place = 1
    InputExample(texts=["Place it down"], label=1),  # place = 1
    InputExample(texts=["Put down the object"], label=1),  # put down = 1
    InputExample(texts=["Put it down"], label=1),  # put down = 1
    InputExample(texts=["Leave it"], label=1),  # leave = 1
    InputExample(texts=["Leave it down"], label=1),  # leave = 1
    InputExample(texts=["Move to home position"], label=2),  # move = 2
    InputExample(texts=["Go home"], label=2),  # go = 2
    InputExample(texts=["Go to home position"], label=2),  # go = 2
    InputExample(texts=["Parking position"], label=2),  # park = 2
]
```
All pick related sentences are with label 0, place related sentences have label 1 and sentences related with home position have label 2. Additional sentences with extra labels can be added in order to enlarge the robot operation.

This model was trained with 500 epochs and with learning rate 2e-3. Values can be adjusted based on learning performance of the NN.

The recorded voice command by microphone is transcribed by speech recognizer and returned transcription is entered for the transformer model in order to obtain embeddings. This embeddings are compared with embeddings created by fine-tuning of the model in previous step with cosine similarity. The closest fitting sentence is selected based on the comparison and label is returned (either 'pick', 'place' or 'home'). This label serves for decision, what shall be executed with via Ycom interface. 
