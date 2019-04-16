# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license.

import os
import argparse
import datetime
import time
import tensorflow as tf
from math import ceil
import numpy
import shutil
from tensorflow.contrib.slim.python.slim.nets import inception_v3
from azureml.core.model import Model

from keras.models import Sequential
from keras.models import model_from_json
from keras.layers import Dense

slim = tf.contrib.slim

print("begin")

print("1")
parser = argparse.ArgumentParser(description="Start a keras model serving")
print("2")
parser.add_argument('--input_dir', dest="input_dir", required=True)
print("3")
parser.add_argument('--output_dir', dest="output_dir", required=True)
print("4")

args = parser.parse_args()


print("args.input_dir:", args.input_dir)
print("args.output_dir:", args.output_dir)


numpy.random.seed(7)

# get input data
input_data_path = os.path.join(args.input_dir, "pima-indians-diabetes.data.csv")
print("input_data_path:", input_data_path)
dataset = numpy.loadtxt(input_data_path, delimiter=",")
print("dataset:", dataset)
X = dataset[:,0:8]
print("X:", X)

# load model
model_path = Model.get_model_path("keras")
print("model_path:", model_path)
input_model_json_path = os.path.join(model_path, "model.json")
print("input_model_json_path:", input_model_json_path)
json_file = open(input_model_json_path, 'r')
print("json_file:", json_file)
loaded_model_json = json_file.read()
print("loaded_model_json:", loaded_model_json)
json_file.close()
loaded_model = model_from_json(loaded_model_json)
print("loaded_model:", loaded_model)
input_model_weights_path = os.path.join(model_path, "weights.h5")
print("input_model_weights_path:", input_model_weights_path)
loaded_model.load_weights(input_model_weights_path)

# make predictions
predictions = loaded_model.predict(X)
##print("predictions:", predictions)
rounded = [round(x[0]) for x in predictions]
##print("rounded:", rounded)

# write output data
os.makedirs(args.output_dir, exist_ok=True)
out_filename = os.path.join(args.output_dir, "result-labels.txt")
print("out_filename:", out_filename)
json_file = open(out_filename, 'w')
print("json_file:", json_file)
for roundedValue in rounded:
    json_file.write(str(roundedValue) + "\n")
json_file.flush() # don't forget to flush, or file contents might not be written!!!
json_file.close()

# copy the file to artifacts
shutil.copy(out_filename, "./outputs/")
# Move the processed data out of the blob so that the next run can process the data.

print("end")