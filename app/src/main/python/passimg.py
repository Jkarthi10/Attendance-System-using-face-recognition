import numpy as np
import cv2
from PIL import Image
import base64
import io
import firebase_admin
from firebase_admin import credentials, initialize_app, storage
import sys
import face_recognition
import pickle
import datetime as dt
from os.path import dirname, join
from com.chaquo.python import Python

cred = credentials.Certificate({
                                 "type": "service_account",
                                 "project_id": "attendencesystem-c5512",
                                 "private_key_id": "ac9ec077f013f53d6a0d2cbccef47e1bf4604f0a",
                                 "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDbgYB3EH8Z2zlk\nmZVFXZGJeiuguVEiIUIp3BG4wZi14bO1F5YJzxGN5xBA1HEBAsmG34bBhNDRVunm\n0IGS+6t6KO9LKnHvldyoyDfTyLM809/hxDMm+egHKfERPIK2FJ81wXhu2/yIxJdG\nMJrnU1RBJmzYpoibtv7aXgxARZnuphLxc6uvUU5TSgmEB6FvW9zxh0L0fQ/CDNTQ\nN1F1UAnJui8x/eLPbT2DbdB/4UHcMOc/dCof9eGC27Q7ap5l4FAM3su28nRgm9gk\nnUnEYub/2D4LwonRkWdCxbgK2l3/GwByF+FEuEUZDME8zzaOq3RPSOyEjs4Y8ZuX\n/7Nk4H5nAgMBAAECggEAB5EUxRtKo7EKGZzZEkg8nUZwB5KBKKczLoSOuyrioUPJ\nBpvsCPrcNOM7Yl4QZoOv6m19KeGdXddcU8pp6mUGOb1R1mpS/Xp8iKLyQw40Q4td\njdz4vcYNSLtE5fO14SH1L7deIprZvzs2UxiXgRQ/H3R8JGcakXJC9x3D2AQDikBF\n8JIqd+c6ilrWuX0s5ESYi4dW3fdYh5ZLsU6FaAYL2M0K9EzHBw4B0GBDvV19cEir\nSj/FabERscI5A3YNnHQIxuZtPC2bkfCEBhyXbJs0HYwJP2TzD7r7xUJ/DXIow7Pi\ncrPzkJWm7vCcJKtlQFp8rUskey/8SMYeYZpVv9jueQKBgQD/xe6uIAsuYL8vxD0I\nUGzs1TfiKNyZfbF/4ZmFHktG9RWY5kOERoOvbgJp21t+U1erWN5kUX9nWllcP7j5\nzMUxfUaZ2X81LxoRUj+e+tI0koFJOdidXS6Llihzf2E6nS2VSHgaWDqrlsAjfehA\nwAqYeBl5JqGC0fJIj2AzSkAwrwKBgQDbs1X1ttFb4deJp3pAa2xTE/6Tnu/vUKve\nKkp3w2RWyDp5s4l+MBs4oz6gwlYeIzXv5M2GVbUnZnvMEtcy9c0JkS0/L8rLDtKO\naeTsu9u+aQQ4l0Tr58slh2Dt5v1fiADt/rn6uVxIXT1w+RrBLm3TRbU6Gtj51I8f\nsfy9EPlLyQKBgQDy0ex4rr8utnaLWJhArmnapcm6EeTsa2H58CmZMVtx7/cjA2gR\nygf2ok/0Q2YnFeRjLalkP+LeMe4oH+7yaC7FfxNpuAyGZ0MuMpFn0uOBOZ038Yzu\nSKqJpnKcw8+An/vIf9ZV3HFGuYWLrFq0Lh1hBpPYao5m7f5AWK2Rw+oQzQKBgDVu\nuVJIQ0TIeYZGECqItdDCxSCcABjBEvu2Z2QXRlkA24/rxV3GT2iH81xfx1gPEjgk\n+oNYZvWNLECmuGXxeAuCnnGGqxiVo0n1oTKeQcRegCNPTvjc6ABZm45gpnDMgAVh\n9VNwL2x+GMpYG1SueRFwG7JlAy5HrwNzY1eMQEVZAoGAHEcbcEbZ6tPaUF9KwbBG\n+lho4rC5KuHQIUr0VbHNB3fw+VroBbQBqxOrzUBHbrMqavCPS3B/BusEIKYI38Nr\ns56hSP7A/FAOUaLDo33rtISZzoiaa8fT9HdLh6cse7TvdxeX/Wlv5NVJ3u05yQX9\nntKr/BNor5mfyVRmttZxk3U=\n-----END PRIVATE KEY-----\n",
                                 "client_email": "firebase-adminsdk-q154a@attendencesystem-c5512.iam.gserviceaccount.com",
                                 "client_id": "106697713453270146888",
                                 "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                                 "token_uri": "https://oauth2.googleapis.com/token",
                                 "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                                 "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-q154a%40attendencesystem-c5512.iam.gserviceaccount.com"
                               })
initialize_app(cred, {'storageBucket': 'attendencesystem-c5512.appspot.com'})

files_dir = str(Python.getPlatform().getApplication().getFilesDir())
current_datetime = dt.date.today()
str_current_date = str(current_datetime)
#file_name = "Attendence " + str_current_date + ".csv"
#file = open(file_name, 'w')
filename = join(dirname(files_dir), "Attendence " + str_current_date + ".csv")
with open(filename, 'w+') as f:
    f.writelines(f'{"Name"}, {"Date"}')


def Attendence(name):
    with open(filename, 'r+') as f :
        mydatalist = f.readlines()
        namelist = []
        for line in mydatalist:
            entry = line.split(',')
            namelist.append(entry[0])
        if name not in namelist:
            now = dt.date.today()
            f.writelines(f'\n{name}, {now}')

def main(data):

    decoded_data = base64.b64decode(data)
    np_data = np.fromstring(decoded_data, np.uint8)
    img = cv2.imdecode(np_data, cv2.IMREAD_UNCHANGED)
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    boxes = face_recognition.face_locations(rgb, model="hog")
    encodings = face_recognition.face_encodings(rgb, boxes)
    names = []

    bucket = storage.bucket()
    blob = bucket.get_blob('Year 3/encodings')
    filename_pickle = join(dirname(files_dir), "encodings")
    with open(filename_pickle, 'wb') as fin:
        blob.download_to_file(fin)
        fin.close()

    #blob.download_to_filename(filename="encodings")
    data = pickle.loads(open(filename_pickle, "rb").read())

    for encoding in encodings:
        matches = face_recognition.compare_faces(data["encoding"], encoding)
        name = "Unknown"
        if True in matches:
            matchedIdxs = [i for (i, b) in enumerate(matches) if b]
            counts = {}
            for i in matchedIdxs:
                name = data["names"][i]
                counts[name] = counts.get(name, 0)+1
                name = max(counts, key=counts.get)

            names.append(name)
            Attendence(name)

        blob = bucket.blob('Year 3/'+ "Attendence " + str_current_date + ".csv")
        blob.upload_from_filename(filename)

    return ""+"done"
    '''img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    pil_im = Image.fromarray(img_gray)

    buff = io.BytesIO()
    pil_im.save(buff, format="PNG")
    img_str = base64.b64encode(buff.getvalue())
    return ""+str(img_str, 'utf-8')'''