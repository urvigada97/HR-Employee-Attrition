# import json
# import logging
# import os
# import joblib
# import pytest
# from prediction_service.prediction import form_response, api_response
# import prediction_service
#
# input_data = {
#     "incorrect_range":
#         {
#             "Age": 20,
#             "DailyRate": 105,
#             "DistanceFromHome": 20,
#             "Education": 1,
#             "EmployeeCount": 0.5,
#             "EnvironmentSatisfaction": 1,
#             "HourlyRate": 50,
#             "JobInvolvement": 1,
#             "JobLevel": 4,
#             "JobSatisfaction": 1,
#             "MonthlyIncome": 1010,
#             "MonthlyRate": 2095,
#             "NumCompaniesWorked": 5,
#             "PercentSalaryHike": 20,
#             "PerformanceRating": 1,
#             "RelationshipSatisfaction": 1,
#             "StockOptionLevel": 2,
#             "TotalWorkingYears": 20,
#             "TrainingTimesLastYear": 5,
#             "WorkLifeBalance": 1,
#             "YearsAtCompany": 20,
#             "YearsInCurrentRole": 10,
#             "YearsSinceLastPromotion": 10,
#             "YearsWithCurrManager": 15,
#             "Gender_Male": 0,
#             "OverTime_Yes": 1,
#             "BusinessTravel_Travel_Frequently": 0,
#             "BusinessTravel_Travel_Rarely": 1,
#             "Department_Research_&_Development": 0,
#             "Department_Sales": 1,
#             "EducationField_Life_Sciences": 1,
#             "EducationField_Marketing": 0,
#             "EducationField_Medical": 0,
#             "EducationField_Other": 0,
#             "EducationField_Technical_Degree": 0,
#             "JobRole_Human_Resources": 0,
#             "JobRole_Laboratory_Technician": 0,
#             "JobRole_Manager": 0,
#             "JobRole_Manufacturing_Director": 0,
#             "JobRole_Research_Director": 0,
#             "JobRole_Research_Scientist": 0,
#             "JobRole_Sales_Executive": 1,
#             "JobRole_Sales_Representative": 0,
#             "MaritalStatus_Married": 0,
#             "MaritalStatus_Single": 2
#         },
#
#     "correct_range":
#         {
#             "Age": 20,
#             "DailyRate": 105,
#             "DistanceFromHome": 20,
#             "Education": 1,
#             "EmployeeCount": 0.5,
#             "EnvironmentSatisfaction": 1,
#             "HourlyRate": 50,
#             "JobInvolvement": 1,
#             "JobLevel": 4,
#             "JobSatisfaction": 1,
#             "MonthlyIncome": 1010,
#             "MonthlyRate": 2095,
#             "NumCompaniesWorked": 5,
#             "PercentSalaryHike": 20,
#             "PerformanceRating": 1,
#             "RelationshipSatisfaction": 1,
#             "StockOptionLevel": 2,
#             "TotalWorkingYears": 20,
#             "TrainingTimesLastYear": 5,
#             "WorkLifeBalance": 1,
#             "YearsAtCompany": 20,
#             "YearsInCurrentRole": 10,
#             "YearsSinceLastPromotion": 10,
#             "YearsWithCurrManager": 15,
#             "Gender_Male": 0,
#             "OverTime_Yes": 1,
#             "BusinessTravel_Travel_Frequently": 0,
#             "BusinessTravel_Travel_Rarely": 1,
#             "Department_Research_&_Development": 0,
#             "Department_Sales": 1,
#             "EducationField_Life_Sciences": 1,
#             "EducationField_Marketing": 0,
#             "EducationField_Medical": 0,
#             "EducationField_Other": 0,
#             "EducationField_Technical_Degree": 0,
#             "JobRole_Human_Resources": 0,
#             "JobRole_Laboratory_Technician": 0,
#             "JobRole_Manager": 0,
#             "JobRole_Manufacturing_Director": 0,
#             "JobRole_Research_Director": 0,
#             "JobRole_Research_Scientist": 0,
#             "JobRole_Sales_Executive": 1,
#             "JobRole_Sales_Representative": 0,
#             "MaritalStatus_Married": 0,
#             "MaritalStatus_Single": 1
#         },
#
#     "incorrect_col":
#     {"fixed acidity": 5,
#     "volatile acidity": 1,
#     "citric acid": 0.5,
#     "residual sugar": 10,
#     "chlorides": 0.5,
#     "free sulfur dioxide": 3,
#     "total_sulfur dioxide": 75,
#     "density": 1,
#     "pH": 3,
#     "sulphates": 1,
#     "alcohol": 9
#     }
# }
#
# TARGET_range = {
#     "min": 3.0,
#     "max": 8.0
# }
#
# def test_form_response_correct_range(data=input_data["correct_range"]):
#     res = form_response(data)
#     assert TARGET_range["min"] <= res <= TARGET_range["max"]
#
# def test_api_response_correct_range(data=input_data["correct_range"]):
#     res = api_response(data)
#     assert TARGET_range["min"] <= res["response"] <= TARGET_range["max"]
#
# def test_form_response_incorrect_range(data=input_data["incorrect_range"]):
#     with pytest.raises(prediction_service.prediction.NotInRange):
#         res = form_response(data)
#
# def test_api_response_incorrect_range(data=input_data["incorrect_range"]):
#     res = api_response(data)
#     assert res["response"]==prediction_service.prediction.NotInRange().message
#
# def test_response_incorrect_col(data=input_data["incorrect_col"]):
#     res = api_response(data)
#     assert res["response"] == prediction_service.prediction.NotInCols().message