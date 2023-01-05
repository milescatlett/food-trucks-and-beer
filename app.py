import os
from flask import Flask, request, render_template
import func
import db
from datetime import datetime

project_root = os.path.dirname(os.path.realpath('__file__'))
template_path = os.path.join(project_root, 'templates')
static_path = os.path.join(project_root, 'static')
app = Flask(__name__, template_folder=template_path, static_folder=static_path)


@app.route('/scrape-fhtr', methods=['GET'])
def fhtr():
    if request.method == 'GET':
        ftb = func.fht()
        db.add_scrape(ftb)
        msg = ftb
    return render_template('index.html', msg=msg)


@app.route('/')
def home():
    predata = db.get_entries()
    data = []
    for j in range(len(predata)):
        data.append([predata[j][0], predata[j][1], predata[j][2], predata[j][3], predata[j][0].replace(" ", "-"),
                     predata[j][1].replace(" ", "-")])
    breweries = set()
    food_trucks = set()
    for i in range(len(predata)):
        bpd = predata[i][0].replace(" ", "-")
        ftpd = predata[i][1].replace(" ", "-")
        breweries.add((predata[i][0], bpd))
        food_trucks.add((predata[i][1], ftpd))
    breweries = list(breweries)
    food_trucks = list(food_trucks)
    b_len = len(breweries)
    f_len = len(food_trucks)
    length = len(data)
    return render_template('home.html', data=data, length=length, breweries=breweries, b_len=b_len,
                           food_trucks=food_trucks, f_len=f_len)


@app.route('/scrape-wmb', methods=['GET', 'POST'])
def wmb():
    if request.method == 'POST':
        ftb = request.form['body']
        splitup = ftb.split("@")
        output = []
        for i in range(len(splitup) - 1):
            lst = splitup[i].split("#")
            brewery = lst[0]
            food_truck = lst[1]
            start = datetime.strptime(lst[2], '%Y-%m-%d %H:%M:%S')
            end = datetime.strptime(lst[3], '%Y-%m-%d %H:%M:%S')
            eid = lst[4]
            uid = int(lst[5]) + db.get_eid()
            output.append((brewery, food_truck, start, end, eid, uid))
        db.add_scrape(output)
    return render_template('wmb.html')


application = app