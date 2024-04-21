from flask import Flask, render_template, request
import pickle

app = Flask(__name__)

# Load the saved model from the file
with open('Logistic Regression.pkl', 'rb') as file:
    loaded_model = pickle.load(file)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get data from the request
        data=[]
        values=[]
        for field_names,field_value in request.form.items():
            values.append(field_value)
       
        # Make predictions
        to_numeric = {'male': 1, 'female': 2,
              'yes': 1, 'no': 2,
              'graduated': 1, 'not-graduated': 2,
              'urban': 3, 'semiurban': 2,'rural': 1,
              'Y': 1, 'N': 0,
              '3+': 3}
        values[-2] = 1.0 if float(values[-2]) >= 700 else 0.0
        values[6]=float(values[6])/10
        values[7]=float(values[7])/10
        values[8]=float(values[8])/1000
        value_to_move = values.pop(3)  # Remove value at index 2 and return it
        values.append(value_to_move)
        data.append(values)
        preditction_data=[[to_numeric.get(value, value) for value in sublist] for sublist in data]
        del preditction_data[0][0]
        float_list = [[float(item) for item in sublist] for sublist in preditction_data]
        predictions = loaded_model.predict(float_list)
        # Return pr
        # edictions as JSON response
        if predictions==1:
            result='Approved'
        else:
            result='Rejected'
        return render_template('result.html', result=result)
    except Exception as e:
        return render_template('result.html',result=e)
   
if __name__ == '__main__':
    app.run(host='0.0.0.0')