from flask import Flask, render_template, request, flash
import pandas as pd
import pickle
import numpy as np

from utils import validate_inputs

app = Flask(__name__)

# Load model (asumsi model sudah dilatih dan disimpan dalam file pickle)
knn_model = pickle.load(open('models/knn_best_model.pkl', 'rb'))
scaler_model = pickle.load(open('models/robust_scaler_model.pkl', 'rb'))

# Load dataset untuk ditampilkan di halaman Dataset
df = pd.read_excel("Rice_Cammeo_Osmancik.xlsx")

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/dataset')
def dataset():
    sample_data = df.head(10)  # Ambil 10 sampel data
    return render_template('dataset.html', tables=[sample_data.to_html(classes='data', header="true")])

@app.route('/klasifikasi', methods=['GET', 'POST'])
def classify():
    
    result = None
    if request.method == 'POST':
        # Ambil input dari form
        area = request.form['Area']
        perimeter = request.form['Perimeter']
        major_axis = request.form['Major_Axis']
        minor_axis = request.form['Minor_Axis']
        eccentricity = request.form['Eccentricity']
        convex_area = request.form['Convex_Area']
        extent= request.form['Extent']
        
        # result = [area, perimeter, major_axis, minor_axis, eccentricity, convex_area, extent]
        # return result
        
        raw_data = {
            "Area": area,
            "Perimeter": perimeter,
            "Major_Axis_Length": major_axis,
            "Minor_Axis_Length": minor_axis,
            "Eccentricity": eccentricity,
            "Convex_Area": convex_area,
            "Extent": extent
            }
        
        is_valid, warning_message  = validate_inputs(raw_data)
        print(warning_message)
        
        if is_valid:   
            # convert input to DF
            form_df = pd.DataFrame([raw_data])
            
            
            # scaling
            scaled_input = scaler_model.transform(form_df)
            print(scaled_input)
                
            # classify    
            prediction = knn_model.predict(np.array(scaled_input))
            print(type(prediction))
                
            result = "Cammeo" if prediction[0] == 0 else "Osmancik"
            # if form_df is not None and not form_df.empty:
        else: 
            return render_template('classify.html', error=warning_message)
        
    return render_template('classify.html', result=result)

@app.route('/tentang')
def about():
    return render_template('about.html')

@app.route("/base")
def base():
    return render_template('base.html')
@app.route("/child")
def child():
    return render_template('child.html')

if __name__ == '__main__':
    app.run(debug=True)
