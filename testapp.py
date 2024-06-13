from flask import Flask, render_template, request, jsonify
import pickle
import numpy as np
import pandas as pd

app = Flask(__name__)


@app.route('/')
def career():
    return render_template("hometest.html")


@app.route('/predict', methods=['POST', 'GET'])
def result():
    if request.method == 'POST':
        try:
            result = request.form
            print(result)
            res = result.to_dict(flat=True)
            print("res:", res)

            # Convert form data to a list of values
            arr = list(res.values())

            # Convert the list of string values to numeric values using pandas
            numeric_data = pd.to_numeric(pd.Series(arr), errors='coerce')

            # Handle NaN values in the pandas Series by replacing them with 0
            numeric_data = numeric_data.fillna(0)

            # Convert the pandas Series to a numpy array
            data = numeric_data.to_numpy()

            # Reshape the array to match the model's expected input
            data = data.reshape(1, -1)
            print(data)

            # Load the pre-trained model
            loaded_model = pickle.load(open("careerlast.pkl", 'rb'))

            # Make predictions
            predictions = loaded_model.predict(data)
            print(predictions)

            # Get prediction probabilities
            pred_proba = loaded_model.predict_proba(data)
            print(pred_proba)

            # Process the probabilities to determine likely job categories
            pred = pred_proba > 0.05
            i = 0
            j = 0
            index = 0
            res = {}
            final_res = {}

            while j < 17:
                if pred[i, j]:
                    res[index] = j
                    index += 1
                j += 1

            index = 0
            for key, values in res.items():
                if values != predictions[0]:
                    final_res[index] = values
                    print('final_res[index]:', final_res[index])
                    index += 1

            jobs_dict = {
                0: 'AI ML Specialist',
                1: 'API Integration Specialist',
                2: 'Application Support Engineer',
                3: 'Business Analyst',
                4: 'Customer Service Executive',
                5: 'Cyber Security Specialist',
                6: 'Data Scientist',
                7: 'Database Administrator',
                8: 'Graphics Designer',
                9: 'Hardware Engineer',
                10: 'Helpdesk Engineer',
                11: 'Information Security Specialist',
                12: 'Networking Engineer',
                13: 'Project Manager',
                14: 'Software Developer',
                15: 'Software Tester',
                16: 'Technical Writer'
            }

            job = predictions[0]
            print(job)

            return render_template("testafter.html", final_res=final_res, job_dict=jobs_dict, job0=job)
        except Exception as e:
            print("Error occurred:", e)
            return jsonify({'error': str(e)}), 500
    else:
        return "Please submit a POST request.", 400

      
if __name__ == '__main__':
   app.run(debug = True)
