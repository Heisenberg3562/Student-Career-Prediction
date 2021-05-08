from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from sklearn.preprocessing import Normalizer
import joblib
import pandas as pd


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
        criteria = {}
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
        for i,j in zip(range(len(request.GET)-1),columns):
            li.append(int(request.GET['input'+str(i)]))
        normalized_data = Normalizer().fit_transform([li])
        for i,j in zip(range(len(request.POST)-1),columns):
            input[j] = normalized_data[0][i]
        df = pd.DataFrame(input,index=[0])
        model = joblib.load('static/svm.pkl')
        labelencoder = joblib.load('static/label.pkl')
        results = model.predict(df)
        prediction = labelencoder.inverse_transform(results)
        criteria['prediction'] = prediction[0]
    return JsonResponse(criteria, safe=False)
