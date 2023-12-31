

from __future__ import division, print_function
# coding=utf-8
import sys
import os
import glob
import re
import numpy as np
import tensorflow as tf
import tensorflow as tf

from tensorflow.compat.v1 import ConfigProto
from tensorflow.compat.v1 import InteractiveSession

config = ConfigProto()
config.gpu_options.per_process_gpu_memory_fraction = 0.2
config.gpu_options.allow_growth = True
session = InteractiveSession(config=config)
# Keras
from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

# Flask utils
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename

app = Flask(__name__)


MODEL_PATH ='model_inception.h5'

model = load_model(MODEL_PATH)




def model_predict(img_path, model):
    print(img_path)
    img = image.load_img(img_path, target_size=(224, 224))

    # Preprocessing the image
    x = image.img_to_array(img)

    ## Scaling
    x=x/255
    x = np.expand_dims(x, axis=0)
   

    preds = model.predict(x)
    print(preds)
    preds=np.argmax(preds, axis=1)
    if preds==0:
        preds="This belongs to Keyboard category"
    elif preds==1:
        preds="This belongs to Laptop category"
    elif preds==2:
        preds="This belongs to Mobile category"
    elif preds==3:
        preds="This belongs to Monitor category"
    elif preds==4:
        preds="This belongs to Mouse category"
    elif preds==5:
        preds="This belongs to Router category"    
    
    return preds


@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)

        # Make prediction
        preds = model_predict(file_path, model)
        result=preds
        # os.remove(f.filename)
        return result
    return None


if __name__ == '__main__':
    app.run(port=5001,debug=True)
