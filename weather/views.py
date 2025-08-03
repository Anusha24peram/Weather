import pandas as pd
import os
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse
from sklearn.preprocessing import StandardScaler

def home(request):
    return HttpResponse('<h2>Welcome to Weather App</h2><a href="/process/">Go to Weather Processing</a>')

def process_weather_data(request):
    # CSV path inside the app folder
    csv_file_path = os.path.join(settings.BASE_DIR, 'weather', 'seattle-weather.csv')
    df = pd.read_csv(csv_file_path)

    shape_before = df.shape
    df = df.drop_duplicates()

    # Replace 0 values with mean
    for col in ['precipitation', 'temp_max', 'temp_min', 'wind']:
        df[col] = df[col].replace(0, df[col].mean())

    # Count remaining 0s
    missing_counts = {
        'precipitation': (df['precipitation'] == 0).sum(),
        'temp_max': (df['temp_max'] == 0).sum(),
        'temp_min': (df['temp_min'] == 0).sum(),
        'wind': (df['wind'] == 0).sum(),
    }

    # Feature & Label Split
    if 'Outcome' in df.columns:
        x = df.drop(columns='Outcome')
        y = df['Outcome']
    else:
        x = df.iloc[:, :-1]
        y = df.iloc[:, -1]

    scaler = StandardScaler()
    x_scaled = scaler.fit_transform(x)

    return render(request, 'result.html', {
        'shape_before': shape_before,
        'head': df.head().to_html(),
        'tail': df.tail().to_html(),
        'describe': df.describe().to_html(),
        'missing_counts': missing_counts,
        'x_scaled': x_scaled[:5].tolist(),
        'y': y.head().tolist(),
    })

