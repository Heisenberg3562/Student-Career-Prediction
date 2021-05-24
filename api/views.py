from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from sklearn.preprocessing import Normalizer
import joblib
import pandas as pd
import numpy as np


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
