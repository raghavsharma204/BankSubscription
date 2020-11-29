from flask import Flask, render_template, request
import sqlite3 as sql
import pandas as pd
from sqlite3 import Error
import pickle
import numpy as np
from sklearn.preprocessing import LabelEncoder
import pickle

app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))

@app.route('/')
def home():
    return render_template("Home.html")


def get_integer_mapping(le):
    '''
    Return a dict mapping labels to their integer values
    from an SKlearn LabelEncoder
    le = a fitted SKlearn LabelEncoder
    '''
    res = {}
    for cl in le.classes_:
        res.update({cl:le.transform([cl])[0]})

    return res


@app.route("/checkforrecord", methods=["POST", "GET"])
def checkApplicant():
    msg = ''
    if request.method == "POST":
        #print("inside if")
        try:
            print("inside try")
            age = request.form["Age"]
            job = request.form["Job"]
            marital = request.form["Marital"]
            education = request.form["Education"]
            default = request.form["Default"]
            balance = request.form["Balance"]
            housing = request.form["Housing"]
            loan = request.form["Loan"]
            contact = request.form["Contact"]
            day = request.form["Day"]
            month = request.form["Month"]
            duration = request.form["Duration"]
            campaign = request.form["Campaign"]
            pdays = request.form["Pdays"]
            previous = request.form["Previous"]
            poutcome = request.form["Poutcome"]
            print('age is' , age)

            df = pd.read_csv('dataset_formatted')

            job = get_integer_mapping(LabelEncoder().fit(df['job']))[job]
            marital = get_integer_mapping(LabelEncoder().fit(df['marital']))[marital]
            #print('marital is', marital)
            education = get_integer_mapping(LabelEncoder().fit(df['education']))[education]
            default = get_integer_mapping(LabelEncoder().fit(df['default']))[default]
            housing = get_integer_mapping(LabelEncoder().fit(df['housing']))[housing]
            loan = get_integer_mapping(LabelEncoder().fit(df['loan']))[loan]
            contact = get_integer_mapping(LabelEncoder().fit(df['contact']))[contact]
            month = get_integer_mapping(LabelEncoder().fit(df['month']))[month]
            poutcome = get_integer_mapping(LabelEncoder().fit(df['poutcome']))[poutcome]
            print("done till feats")
            feats = [age , job, marital , education , default , balance , housing, loan , contact , day , month , duration , campaign , pdays , previous , poutcome]
            final_feats = np.array(feats)
            print("done till pred")
            predicitonVal = model.predict(final_feats.reshape(1,-1))
            print("prediction is ", predicitonVal)
            if predicitonVal == 1:
                returnmsg = 'The client will subscribe to a term deposit'
            else:
                returnmsg = 'The client will not subscribe to the term deposit'
            msg = returnmsg

        except:
            msg = "Error occured. Try again"
        return render_template("Success.html", msg=msg)

if __name__ == '__main__':
    app.run(debug=True)


