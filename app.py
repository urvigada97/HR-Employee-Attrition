from flask import Flask, render_template, request, jsonify
import os
import numpy as np
# from prediction_service import prediction
import yaml
import joblib
import pandas as pd

params_path = "params.yaml"
webapp_root = "webapp"

static_dir = os.path.join(webapp_root, "static")
template_dir = os.path.join(webapp_root, "templates")

app = Flask(__name__, static_folder=static_dir,template_folder=template_dir)

def read_params(config_path):
    with open(config_path) as yaml_file:
        config = yaml.safe_load(yaml_file)
    return config

def predict(data):
    config = read_params(params_path)
    model_dir = config["model_dir"]
    scale_model_path = os.path.join(model_dir, "scaler.joblib")
    scaler = joblib.load(scale_model_path)
    data = pd.DataFrame(data, index=[0])
    # print(pd.DataFrame(data, index=[0]))
    feature_not_to_scale = config["preprocess"]["feature_not_to_scale"]
    feature_not_to_scale.remove('Attrition')
    continuous_feature = config["preprocess"]["continuous_feature1"]
    scaled_data = pd.concat([data[feature_not_to_scale].reset_index(drop=True),
               pd.DataFrame(scaler.transform(data[continuous_feature]), columns=continuous_feature)],
              axis=1)
    model_dir_path = config["webapp_model_dir"]
    model = joblib.load(model_dir_path)
    prediction = model.predict(scaled_data)
    print(prediction)
    return prediction

def api_response(request):
    try:
        response = predict(request.json)
        if response == 1:
            response = 'Yes'
        else:
            response = 'No'
        response = {"response": response}
        return response
    except Exception as e:
        print(e)
        error = {"error": "Something went wrong!! Try again later!"}
        return error


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            if request.form:
                dict_req = dict(request.form)
                dict_req['BusinessTravel_Travel_Frequently'] = 0
                dict_req['BusinessTravel_Travel_Rarely'] = 0
                dict_req['Department_Research_&_Development'] = 0
                dict_req['Department_Sales'] = 0
                dict_req['EducationField_Life_Sciences'] = 0
                dict_req['EducationField_Marketing'] = 0
                dict_req['EducationField_Medical'] = 0
                dict_req['EducationField_Other'] = 0
                dict_req['EducationField_Technical_Degree'] = 0
                dict_req['JobRole_Human_Resources'] = 0
                dict_req['JobRole_Laboratory_Technician'] = 0
                dict_req['JobRole_Manager'] = 0
                dict_req['JobRole_Manufacturing_Director'] = 0
                dict_req['JobRole_Research_Director'] = 0
                dict_req['JobRole_Research_Scientist'] = 0
                dict_req['JobRole_Sales_Executive'] = 0
                dict_req['JobRole_Sales_Representative'] = 0
                dict_req['MaritalStatus_Married'] = 0
                dict_req['MaritalStatus_Single'] = 0

                if dict_req['BusinessTravel'] == 'Travel_Rarely':
                    dict_req['BusinessTravel_Travel_Rarely'] = 1
                elif dict_req['BusinessTravel'] == 'Travel_Frequently':
                    dict_req['BusinessTravel_Travel_Frequently'] = 1
                del dict_req['BusinessTravel']

                if dict_req['Department'] == 'Sales':
                    dict_req['Department_Sales'] = 1
                elif dict_req['Department'] == 'Research_&_Development':
                    dict_req['Department_Research_&_Development'] = 1
                del dict_req['Department']

                if dict_req['EducationField'] == 'Life_Sciences':
                    dict_req['EducationField_Life_Sciences'] = 1
                elif dict_req['EducationField'] == 'Marketing':
                    dict_req['EducationField_Marketing'] = 1
                elif dict_req['EducationField'] == 'Medical':
                    dict_req['EducationField_Medical'] = 1
                elif dict_req['EducationField'] == 'Other':
                    dict_req['EducationField_Other'] = 1
                elif dict_req['EducationField'] == 'Technical_Degree':
                    dict_req['EducationField_Technical_Degree'] = 1
                del dict_req['EducationField']

                if dict_req['JobRole'] == 'Human_Resources':
                    dict_req['JobRole_Human_Resources'] = 1
                elif dict_req['JobRole'] == 'Laboratory_Technician':
                    dict_req['JobRole_Laboratory_Technician'] = 1
                elif dict_req['JobRole'] == 'Manager':
                    dict_req['JobRole_Manager'] = 1
                elif dict_req['JobRole'] == 'Manufacturing_Director':
                    dict_req['JobRole_Manufacturing_Director'] = 1
                elif dict_req['JobRole'] == 'Research_Director':
                    dict_req['JobRole_Research_Director'] = 1
                elif dict_req['JobRole'] == 'Research_Scientist':
                    dict_req['JobRole_Research_Scientist'] = 1
                elif dict_req['JobRole'] == 'Sales_Executive':
                    dict_req['JobRole_Sales_Executive'] = 1
                elif dict_req['JobRole'] == 'Sales_Representative':
                    dict_req['JobRole_Sales_Representative'] = 1
                del dict_req['JobRole']

                if dict_req['MaritalStatus'] == 'Married':
                    dict_req['MaritalStatus_Married'] = 1
                elif dict_req['MaritalStatus'] == 'Single':
                    dict_req['MaritalStatus_Single'] = 1
                del dict_req['MaritalStatus']
                print(dict_req)
                response = predict(dict_req)
                # response = prediction.form_response(dict_req)
                if response==1:
                    response = 'Yes'
                else:
                    response = 'No'
                return render_template("index.html", response=response)
            elif request.json:
                response = api_response(request)
                return jsonify(response)
                # return jsonify({'success':1})
                # response = prediction.api_response(request.json)
                # return jsonify(response)

        except Exception as e:
            print(e)
            error = {"error": "Something went wrong!! Try again later!"}
            error = {"error": e}

            return render_template("404.html", error=error)
    else:
        return render_template("index.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)