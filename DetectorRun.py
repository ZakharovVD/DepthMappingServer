import urllib
from Detector import *
import utils_image as b64img

detector = Detector()


def init_detector():
    # modelURL = "http://download.tensorflow.org/models/object_detection/tf2/20200711/ssd_mobilenet_v2_fpnlite_320x320_coco17_tpu-8.tar.gz"
    # modelURL = "http://download.tensorflow.org/models/object_detection/tf2/20200711/efficientdet_d4_coco17_tpu-32.tar.gz"
    modelURL = "http://download.tensorflow.org/models/object_detection/tf2/20200711/faster_rcnn_resnet50_v1_640x640_coco17_tpu-8.tar.gz"

    classFile = "coco.names"
    global detector
    detector.readClasses(classFile)
    detector.downloadModel(modelURL)
    detector.loadModel()


def detect(imagePath, imageName, outputPath, threshold=0.5):
    return detector.predictImage(os.path.join(imagePath, imageName), outputPath, threshold=threshold)
