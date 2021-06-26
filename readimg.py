import numpy as np
import urllib.request
import cv2


hdr = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
def url_to_image(url):
    req= urllib.request.Request(url,headers = hdr)
    with urllib.request.urlopen(req)as urlresp:
        image = np.asarray(bytearray(urlresp.read()), dtype="uint8")
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)
        # cv2.imshow("Image", image)
        # cv2.waitKey(0)
        return image