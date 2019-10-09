#!/usr/bin/env python
from flask import Flask, render_template, Response, request, jsonify
import cv2
import os
from time import sleep
import json
from watson_developer_cloud import VisualRecognitionV3
from werkzeug.utils import secure_filename

app = Flask(__name__)
video = cv2.VideoCapture(0)

list_product = {}
result = []
flag = 0
count = '0'

price = {'Bottle601':10, 'Bottle602':20, 'Bottle603' : 30 ,
        'Chips401': 10, 'Chips402' : 20, 'Chips403' : 30,
        'Choc301': 5, 'Choc302': 100, 'Choc303' : 300,
        'Drink201' : 20, 'Drink202': 45, 'Drink203':90,
        'Shamp501' : 2, 'Shamp502' : 50, 'Shamp503' : 200,
        'Tooth101' : 20 , 'Tooth102' : 45, 'Tooth103': 150}

def clear():
    global count
    global list_product
    global result
    global flag
    global price

    count = '0'
    list_product = {}
    result = []
    flag = 0

    return 'data cleared'

def item_data_price():

    global count
    global list_product
    global result
    global flag
    global count
    global price

    visual_recognition = VisualRecognitionV3(
        '2018-03-19',
        iam_apikey='MhOB0X6MTF24-rx2QNl-eCqAPxV_9EX05KdPtBZigq0j')

    with open('test1.jpg', 'rb') as images_file:
        classes = visual_recognition.classify(
            images_file,
            threshold='0.6',
            classifier_ids='DefaultCustomModel_1778410211').get_result()
    try:
        print(classes['images'][0]['classifiers'][0]['classes'][0]['class'])
        data = classes['images'][0]['classifiers'][0]['classes'][0]['class']
        res = data.split('_')
        item_id = res[0]
        weight = res[1]
        item_name,item_size = res[2].split()
            
        for product_res in result:
            if product_res['item_id'] == item_id:
                print('comes here')
                product_res['item_id'] = item_id
                product_res['weight'] = weight
                product_res['item_name'] = item_name
                product_res['item_size'] = item_size
                product_res['price'] = price[item_id]
                product_res['quantity'] = product_res['quantity'] + 1
                flag = 1
        if flag == 0:
            list_product['item_id'] = item_id
            list_product['weight'] = weight
            list_product['item_name'] = item_name
            list_product['item_size'] = item_size
            list_product['price'] = price[item_id]
            list_product['quantity'] = 1
            flag = 0
            result.append(list_product)
            list_product = {}
        print(result)
        flag = 0
                   
    except:
        print('item not found')
    count = int(count) + 1
    count = str(count)

    return result

@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')

def gen():
    """Video streaming generator function."""
    while True:
        rval, frame = video.read()
        # print(rval,frame)
        cv2.imwrite('t.jpg', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + open('t.jpg', 'rb').read() + b'\r\n')

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    # print(Response(gen(),mimetype='multipart/x-mixed-replace; boundary=frame'))
    return Response(gen(),mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/btn_new_bill',methods=['GET', 'POST'])
def btn_new_bill():
    print('comes hre')
    if request.method == 'POST':
        data = clear()
        print(data)

    return data

@app.route('/item_data', methods=['GET', 'POST'])
def item_data():

    if request.method == 'POST':
        print('comes hre')
        rval, frame = video.read()
        cv2.imwrite(filename='test1.jpg', img=frame)
        print("Image saved!")
        # Get the file from post request

        res = item_data_price()
         
    return jsonify(result=res)

if __name__ == '__main__':
    app.run(debug=True)
