from flask import Flask, request, render_template
from flask_wtf import FlaskForm
from wtforms import IntegerField, RadioField, FloatField, SubmitField, StringField, PasswordField
from wtforms.validators import DataRequired
import pandas as pd

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretKEY'

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
    alkphos = FloatField('Alkpos', validators=[DataRequired()])
    submit = SubmitField('Predict')


@app.route('/', methods=['GET', 'POST'])
def index():
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

        cols = ['Age', 'Total_Bilirubin', 'Direct_Bilirubin', 'Total_Proteins', 'Albumin', 'Ag_Ratio', 'Sgot', 'Sgpt', 'Alkphos']

        data = [[age, tb, db, tp, alb, ag, sgot, sgpt, alk]]
        data2 = [age, tb, db, tp, alb, ag, sgot, sgpt, alk]

        #data = pd.DataFrame(data, columns=cols)

        return render_template('predict.html', title="Just a trial", form=form, data=data)

    return render_template('predict.html', title="Just a trial", form=form)




if __name__ == '__main__':
    app.run(port=3000, debug=True)