#Using Flask in python as web api to accept data,
# preprocess and predict on the data whether patient
# has kideny disease: Positive or Not: Negative

#import necessary packages
from flask import Flask, request, render_template
from flask_wtf import FlaskForm
import joblib
import pandas as pd
import math
from sklearn.preprocessing import StandardScaler
from wtforms import IntegerField, RadioField, FloatField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = '2ac5a75f4c6fa7283d4b3b0a7fa0f93f'

#load model
model = joblib.load('C:/Users/Ek/flask_blog/jake/ecc/knns.pkl')

#create web form according to the data inputs needed
class InputForm(FlaskForm):
    age = IntegerField('Age', validators=[DataRequired()])
    #gender = RadioField('Gender', choices=['Male', 'Female'], validators=[DataRequired()])
    tot_bilirubin = FloatField('Total Bilirubin', validators=[DataRequired()])
    direct_bilirubin = FloatField('Direct Bilirubin', validators=[DataRequired()])
    tot_proteins = IntegerField('Total Proteins', validators=[DataRequired()])
    albumin = IntegerField('Albumin', validators=[DataRequired()])
    ag_ratio = IntegerField('Ag_Ratio', validators=[DataRequired()])
    sgot = FloatField('Sgot', validators=[DataRequired()])
    sgpt = FloatField('Sgpt', validators=[DataRequired()])
    alkphos = FloatField('Sgpt', validators=[DataRequired()])
    submit = SubmitField('Predict')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    form = InputForm()
    if request.method == 'POST':
        age = form.age.data
        tb = form.tot_bilirubin.data
        db = form.direct_bilirubin.data
        tp = form.tot_proteins.data
        alb = form.albumin.data
        ag = form.ag_ratio.data
        sgot = form.sgot.data
        sgpt = form.sgpt.data
        alk = form.alkphos.data

        cols = ['Age', 'Total_Bilirubin', 'Direct_Bilirubin',
                'Total_Proteins', 'Albumin', 'Ag_Ratio', 'Sgot',
                'Sgpt', 'Alkphos']

        data = [[age, tb, db, tp, alb, ag, sgot, sgpt, alk]]
        #data2 = [age, tb, db, tp, alb, ag, sgot, sgpt, alk]

        data = pd.DataFrame(data, columns=cols)

        #data preprocessing
        # performing log10 transformation of positive skewed fields
        skewed = ['tot_bilirubin', 'direct_bilirubin',
                  'tot_proteins', 'albumin', 'ag_ratio', 'alkphos']
        data[skewed] = data[skewed].applymap(math.log10)

        # scaling age,sgpt and sgot
        # Standardization with StandardScaler
        from sklearn.preprocessing import StandardScaler
        sc = StandardScaler()
        data[['age', 'sgpt', 'sgot']] = sc.fit_transform(data[['age', 'sgpt', 'sgot']])

        #predict on the data
        predict = model.predict(data)



        return render_template('predict.html', title="Just a trial", form=form, predict=predict)

    return render_template('predict.html', title='Liver Disease Prediction', form=form)


if __name__ == '__main__':
    app.run(port=3000, debug=True)