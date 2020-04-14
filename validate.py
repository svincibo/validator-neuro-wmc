#!/usr/bin/env python3

import os
import json
#import re
#import subprocess
#import nibabel
#import numpy as np
#from PIL import Image, ImageDraw
#import io
#import base64
#import math
# Things that this script checks
# 
# * make sure mrinfo runs successfully on specified t1 file
# * make sure t1 is 3d
# * raise warning if t1 transformation matrix isn't unit matrix (identity matrix)

# display where this is running
# import socket
# print(socket.gethostname())

with open('config.json') as config_json:
    config = json.load(config_json)

results = {"errors": [], "warnings": []}

#TODO

with open("product.json", "w") as fp:
    json.dump(results, fp)
print("done");
