import numpy as np
from PIL import Image
import os, cv2


"""
References: https://github.com/ni-chi-Tech/Face-Recognition#local-binary-pattern-histogram-face-recognizer

As any other classifier, the Local Binary Patterns, or LBP in short, also needs to be trained on hundreds of images. LBP is a visual/texture descriptor, and thankfully, our faces are also composed of micro visual patterns. So, LBP features are extracted to form a feature vector that classifies a face from a non-face.

For each block, LBP looks at 9 pixels (3×3 window) at a time, and with a particular interest in the pixel located in the center of the window. Then, it compares the central pixel value with every neighbor's pixel value under the 3×3 window. For each neighbor pixel that is greater than or equal to the center pixel, it sets its value to 1, and for the others, it sets them to 0. After that, it reads the updated pixel values (which can be either 0 or 1) in a clockwise order and forms a binary number. Next, it converts the binary number into a decimal number, and that decimal number is the new value of the center pixel. We do this for every pixel in a block. Then, it converts each block values into a histogram, so now we have gotten one histogram for each block in an image. Finally, it concatenates these block histograms to form a one feature vector for one image, which contains all the features we are interested. So, this is how we extract LBP features from a picture.

"""


# Method to train custom classifier to recognize face
def train_classifer(personName):
    # Read all the images in custom data-set
    path = os.path.join(os.getcwd() + "/data/" + personName + "/")

    faces = []
    ids = []
    labels = []
    pictures = {}

    # Store images in a numpy format and ids of the user on the same index in imageNp and id lists
    for root,dirs,files in os.walk(path):
        pictures = files

    for pic in pictures :
        imgpath = path+pic
        img = Image.open(imgpath).convert('L')
        imageNp = np.array(img, 'uint8')
        id = int(pic.split(personName)[0])
        #names[name].append(id)
        faces.append(imageNp)
        ids.append(id)

    ids = np.array(ids)

    #Train and save classifier
    classifier = cv2.face.LBPHFaceRecognizer_create()
    classifier.train(faces, ids)
    classifier.write("./data/classifiers/"+personName+"_classifier.xml")

