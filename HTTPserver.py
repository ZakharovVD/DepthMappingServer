from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
from pyngrok import ngrok
from pyngrok import conf
import threading
import urllib.parse
import time
import os
import sys
import json

import utils_image as b64img

import Estimator as Estimator
import DetectorRun as Detector

hostName = "localhost"
serverPort = 5050
curThread = 0


class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.print_thread("GET")

    def do_POST(self):
        self.send_response(200)

        headers_json = self.headers
        content_length = int(headers_json['Content-Length'])
        body = self.rfile.read(content_length).decode()
        body_json = urllib.parse.parse_qs(body)

        print(headers_json)
        # print(body_json)

        global curThread
        curThread += 1

        workPath = os.path.join('/content/database', 'thread{}'.format(str(curThread)))

        inputPath = os.path.join(workPath, 'input')
        outputPath = os.path.join(workPath, 'output')

        os.makedirs(inputPath, exist_ok=True)
        os.makedirs(outputPath, exist_ok=True)

        inputName = "input.png"
        predictName = "prediction.png"
        estimateName = "input.png"

        estimatePath = os.path.join(workPath, 'output')

        b64img.pict_save_b64(body_json['Image'][0], os.path.join(inputPath, inputName))
        body_json.__delitem__('Image')

        estimateJson = {}
        if headers_json.get('estimateImage'):
            if headers_json['estimateImage'] == 'True':
                argv = ['--data_dir', inputPath, '--output_dir', outputPath, '--Final', '--depthNet', '2']
                if headers_json.get('maxRes'):
                    argv.append('--max_res')
                    argv.append(headers_json['max_res'])
                if headers_json.get('colorizeResults') == 'True':
                    argv.append('--colorize_results')
                if headers_json.get('countSegmentation'):
                    count_segmentation = int(headers_json['countSegmentation'])

                print(argv)
                Estimator.estimateImage(argv)
                estimateJson['estimateImage'] = b64img.pict_read_b64(os.path.join(outputPath, estimateName))

        predictJson = {}
        if headers_json.get('predictImage'):
            if headers_json['predictImage'] == 'True':
                threshold = 0.4
                if headers_json.get('threshold') is not None:
                    threshold = float(headers_json['threshold'])
                predictJson = {'detectionBoxes': Detector.detect(inputPath, inputName, outputPath, threshold=threshold)}
            if headers_json.get('getPredictImage') == 'True':
                predictJson['predictImage'] = b64img.pict_read_b64(os.path.join(outputPath, predictName))

        estimateJson.update(predictJson)

        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(bytes(json.dumps(estimateJson), "utf-8"))

    def print_thread(self, HttpMethod):
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<html><head><title>DepthModeling</title></head>", "utf-8"))
        self.wfile.write(bytes("<p>Request:  %s  %s</p>" % (HttpMethod, self.path), "utf-8"))
        self.wfile.write(bytes("<p>Thread: %s</p>" % threading.currentThread().getName(), "utf-8"))
        self.wfile.write(bytes("<p>Thread Count: %s</p>" % threading.active_count(), "utf-8"))
        self.wfile.write(bytes("<p>Server works correctly</p>", "utf-8"))


# class ThreadingSimpleServer(ThreadingMixIn, HTTPServer):
class ThreadingSimpleServer(HTTPServer):
    pass


if __name__ == "__main__":
    conf.get_default().auth_token = "222fs4vXjr5BpoPBUDMYX4IkWsj_5GhXBQLRPZDSqfMLyhfCr"
    port = os.environ.get("PORT", serverPort)
    server_address = ('', port)

    webServer = ThreadingSimpleServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    public_url = ngrok.connect(port).public_url
    print("ngrok tunnel \"{}\" -> \"http://127.0.0.1:{}\"".format(public_url, port))
    print(public_url[7::])

    Estimator.setThreshold(3000, 1568)

    Estimator.init_methods("leres")
    Estimator.init_methods("midas")

    Detector.init_detector()

    print("Server has been started")
    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
