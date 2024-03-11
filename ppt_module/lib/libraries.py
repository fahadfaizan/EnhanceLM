import re
import os
import math
import json
import numpy as np
import pandas as pd
import unicodedata
from pptx import Presentation
from pptx.enum.shapes import MSD_SHAPE_TYPE
import traceback
import boto3
import requests
import io
from io import BytesIO
import time
import PIL
from PIL import Image,ImageOps
import cv2

from keras.models import load_model

import warnings
warnings.filterwarnings("ignore")
warnings.filterwarnings("ignore")

