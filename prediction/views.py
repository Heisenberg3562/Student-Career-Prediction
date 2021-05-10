from django.http import HttpResponse
from django.shortcuts import render
from sklearn.preprocessing import Normalizer
import joblib
import pandas as pd

def index(request):
    form = request.POST or None
    criteria = {"name":"Omkar"}
    if form:
        print(request.POST)
        input = dict()
        li = []
        criteria = {"name":"Omkar"}
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
        for i,j in zip(range(len(request.POST)-1),columns):
            li.append(int(request.POST['input'+str(i)]))
        normalized_data = Normalizer().fit_transform([li])
        print(normalized_data)
        for i,j in zip(range(len(request.POST)-1),columns):
            input[j] = normalized_data[0][i]
        print(input)
        df = pd.DataFrame(input,index=[0])
        print(df)
        model = joblib.load('static/svm.pkl')
        labelencoder = joblib.load('static/label.pkl')
        results = model.predict(df)
        print(results)
        prediction = labelencoder.inverse_transform(results)
        print(prediction)
        criteria['prediction'] = prediction[0]

    return render(request, 'index-creative.html', criteria)
