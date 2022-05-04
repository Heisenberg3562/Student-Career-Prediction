from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from sklearn.preprocessing import Normalizer
import joblib
import pandas as pd
import numpy as np
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json


# Create your views here.

@api_view(['GET'])
def apiOverview(request):
    api_urls = {
        'Predict': '/predict/',
    }
    return Response(api_urls)


@api_view(['GET'])
def predict(request):
    form = request.GET or None
    criteria = {}
    if form:
        input = dict()
        li = []
        columns=['Acedamic percentage in Operating Systems', 'percentage in Algorithms',
                       'Percentage in Programming Concepts',
                       'Percentage in Software Engineering', 'Percentage in Computer Networks',
                       'Percentage in Electronics Subjects',
                       'Percentage in Computer Architecture', 'Percentage in Mathematics',
                       'Percentage in Communication skills', 'Hours working per day',
                       'Logical quotient rating', 'hackathons', 'coding skills rating',
                       'public speaking points', 'can work long time before system?',
                       'self-learning capability?', 'Extra-courses did', 'olympiads',
                       'reading and writing skills', 'Management or Technical', 'hard/smart worker',
                       'worked in teams ever?']
        for i in range(len(request.GET)):
            li.append(int(request.GET['input'+str(i)]))
        normalized_data1 = Normalizer().fit_transform([li[:14]])
        normalized_data2 = Normalizer().fit_transform([li[14:]])
        normalized_data = np.append(normalized_data1, normalized_data2, axis=1)
        for i, j in zip(range(len(request.GET)), columns):
            input[j] = normalized_data[0][i]
        df = pd.DataFrame(input, index=[0])
        model = joblib.load('static/svm.pkl')
        labelencoder = joblib.load('static/label.pkl')
        results = model.predict(df)
        prediction = labelencoder.inverse_transform(results)
        criteria['prediction'] = prediction[0]
    return Response(criteria, headers= {'Access-Control-Allow-Origin': '*'})

@api_view(['GET'])
def sheetData(request):
    form = request.GET or None
    criteria = {}
    if form:
        input = dict()
        li = []
        scopes = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ]
        credentials = ServiceAccountCredentials.from_json_keyfile_name("able-keep-294916-cd73b531cd6e.json", scopes)  # access the json key you downloaded earlier
        file = gspread.authorize(credentials)  # authenticate the JSON key with gspread
        # sheet = file.open("Python_MUO_Google_Sheet")  # open sheet
        # sheet = file.open_by_key("1CzKezooHJwkWS8ikI6l_bS8Lvv7dnqL1")
        sheet = file.open_by_key(str(request.GET['sheetId']))
        sheet = sheet.get_worksheet(0)
        # all_cells = sheet.range('A1:C6')
        # print(all_cells)
        records_data = sheet.acell('B30').value
        flag = 0
        rowCount = 6
        # while flag == 0:
        #     print(sheet.acell('D'+str(rowCount)).value)
        #     print(type(sheet.acell('D'+str(rowCount)).value))
        #     if type(sheet.acell('B'+str(rowCount)).value) == str:
        #         records_data[sheet.acell('B' + str(rowCount)).value] = str(sheet.acell('D' + str(rowCount)).value)
        #     else:
        #         flag = 1
        #         break
        #     rowCount += 1
        # records_data = sheet.get_all_records()
        records_data = sheet.get_all_values()
        # records_data = records_data[4:]
        rollno = str(request.GET['rollno']).upper()
        att = ''
        for i in records_data:
            print(i)
            if rollno in i:
                att = i[3]
                break
        # for i in range(len(request.GET)):
        #     li.append(int(request.GET['input'+str(i)]))
        # normalized_data1 = Normalizer().fit_transform([li[:14]])
        # normalized_data2 = Normalizer().fit_transform([li[14:]])
        # normalized_data = np.append(normalized_data1, normalized_data2, axis=1)
        # for i, j in zip(range(len(request.GET)), columns):
        #     input[j] = normalized_data[0][i]
        # df = pd.DataFrame(input, index=[0])
        # model = joblib.load('static/svm.pkl')
        # labelencoder = joblib.load('static/label.pkl')
        # results = model.predict(df)
        # prediction = labelencoder.inverse_transform(results)
        # criteria['prediction'] = prediction[0]
        criteria['Attendance'] = att
    return Response(criteria, headers= {'Access-Control-Allow-Origin': '*'})
