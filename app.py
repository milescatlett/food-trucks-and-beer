"""
Author: Miles Catlett
Date: 12/1/2022
This app imports data from two different brewery websites and creates a filter allowing the user to select a food
truck and/or brewery and see where the two coincide.
"""
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
    """
    Scrapes the Foothills tasking room using a function from func.py
    :return: None
    """
    if request.method == 'GET':
        ftb = func.fht()
        db.add_scrape(ftb)
        msg = ftb
    return render_template('index.html', msg=msg)


@app.route('/')
def home():
    """
    This is the route for the home page where food trucks and breweries are displayed.
    :return: None
    """
    # Get the events from the database
    predata = db.get_entries()
    data = []
    # prepare the data to send it to the templates
    for j in range(len(predata)):
        data.append([predata[j][0], predata[j][1], predata[j][2], predata[j][3], predata[j][0].replace(" ", "-"),
                     predata[j][1].replace(" ", "-")])
    # I used a set to remove duplicates
    breweries = set()
    food_trucks = set()
    # Created lists of breweries and food trucks and corresponding selectors
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
    """
    This route gets data from the Wise Man Brewing site. I am not able to use selenium on my server, so I run the
    program once per month on my desktop Pycharm software and then use this form to upload it.
    :return: None
    """
    if request.method == 'POST':
        ftb = request.form['body']
        # Separate the posted data into chunks
        splitup = ftb.split("@")
        output = []
        # Use a loop to prep the data for entry into the database
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