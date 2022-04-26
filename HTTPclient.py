import http.client
import urllib.parse
import json
import utils_image as b64img

url_address = input()
conn = http.client.HTTPSConnection(url_address)


def send_picture():
    headers = {}
    headers.update({'estimateImage': 'True', 'countSegmentation': '100', 'colorizeResults': 'False'})
    headers.update({'predictImage': 'True', 'getPredictImage': 'True', 'threshold': '0.5'})
    print(headers)

    base64_image = b64img.pict_read_b64('./inputs/sample8.jpg')
    body_json = {'Image': base64_image}
    body = urllib.parse.urlencode(body_json)

    conn.request('POST', '/', body, headers)
    r1 = conn.getresponse()

    print(r1.status, r1.reason)
    response_ = r1.read().decode()

    body_json = json.loads(response_)
    b64img.pict_save_b64(body_json.get("estimateImage"), "output/estimation.png")
    b64img.pict_save_b64(body_json.get("predictImage"), "output/prediction.jpg")

    body_json["estimateImage"] = "B64estimateImageHere"
    body_json["predictImage"] = "B64predictImageHere"

    print(body_json)


if __name__ == "__main__":
    send_picture()
    conn.close()
