from random import randint
from time import strftime
from flask import Flask, render_template, flash, request, jsonify
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField, IntegerField
import joblib
import numpy as np
import pandas as pd


DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = 'SjdnUends821Jsdlkvxh391ksdODnejdDw'

form_model = joblib.load('form_model.pkl')
json_model = joblib.load('json_model.pkl')

rajonai_form = ['Antakalnis', 'Aukštieji Paneriai', 'Avižieniai', 'Bajorai',
                'Balsiai', 'Baltupiai', 'Buivydiškių k.', 'Buivydiškės',
                'Bukiškio k.', 'Burbiškės', 'Didieji Gulbinai', 'Dvarčionys',
                'Fabijoniškės', 'Filaretai', 'Gineitiškės', 'Grigiškės',
                'Jeruzalė', 'Justiniškės', 'Kalnėnai', 'Karoliniškės',
                'Klevinės vs.', 'Lazdynai', 'Lazdynėliai', 'Lentvario m.',
                'Liepkalnis', 'Markučiai', 'Naujamiestis', 'Naujininkai',
                'Naujoji Vilnia', 'Ožkiniai', 'Paneriai', 'Pavilnys',
                'Pašilaičiai', 'Pilaitė', 'Rasos', 'Salininkai', 'Santariškės',
                'Saulėtekis', 'Senamiestis', 'Tarandė', 'Tarandės k.',
                'Trakų Vokė', 'Turniškės', 'Užupis', 'Užusieniai', 'Valakampiai',
                'Verkiai', 'Vilkpėdė', 'Viršuliškės', 'Visoriai', 'Zujūnai',
                'Šeškinė', 'Šiaurės miestelis', 'Šnipiškės', 'Žemieji Paneriai',
                'Žirmūnai', 'Žvėrynas']

rajonai_json = ['Lazdynėliai', 'Bajorai', 'Antakalnis', 'Naujininkai', 'Šnipiškės',
                'Justiniškės', 'Viršuliškės', 'Pilaitė', 'Šiaurės miestelis',
                'Pašilaičiai', 'Šeškinė', 'Fabijoniškės', 'Saulėtekis',
                'Naujamiestis', 'Filaretai', 'Žirmūnai', 'Lazdynai',
                'Karoliniškės', 'Naujoji Vilnia', 'Pavilnys', 'Užupis', 'Rasos',
                'Vilkpėdė', 'Senamiestis', 'Santariškės', 'Žvėrynas', 'Jeruzalė',
                'Baltupiai', 'Visoriai', 'Žemieji Paneriai', 'Salininkai',
                'Balsiai', 'Valakampiai', 'Grigiškės', 'Verkiai', 'Dvarčionys',
                'Markučiai', 'Burbiškės', 'Aukštieji Paneriai', 'Paneriai',
                'Turniškės', 'Avižieniai', 'Bukiškio k.', 'Kalnėnai', 'Liepkalnis',
                'Lentvario m.', 'Trakų Vokė']

gatves = pd.read_csv(
    '/Users/simado/Desktop/api/data/street_data.csv', index_col='Unnamed: 0')
gatves = pd.DataFrame(gatves)


class ReusableForm(Form):
    kambariai = IntegerField('kambariai', validators=[
                             validators.DataRequired()])
    plotas = IntegerField('plotas', validators=[validators.DataRequired()])
    aukstas = IntegerField('aukstas', validators=[validators.DataRequired()])
    aukstu = IntegerField('aukstu', validators=[validators.DataRequired()])
    vardas = TextField('vardas', validators=[validators.DataRequired()])
    email = TextField('email', validators=[validators.DataRequired()])


def get_time():
    time = strftime("%Y-%m-%d %H:%M")
    return time


def log_form(rajonas, kambariai, plotas, aukstas, aukstu, vardas, email, prediction):
    data = open('form_log.log', 'a')
    timestamp = get_time()
    data.write('DateStamp={}, Rajonas={}, Kambariai={}, Plotas={}, Aukštas={}, Aukštų={}, Vardas={}, Email={}, Kaina={} \n'.format(
        timestamp, rajonas, kambariai, plotas, aukstas, aukstu, vardas, email, prediction))
    data.close()


def log_json(rajonas, gatve, kambariai, plotas, aukstas, aukstu, prediction):
    data = open('json_log.log', 'a')
    timestamp = get_time()
    data.write('DateStamp={}, Rajonas={}, Gatve={}, Kambariai={}, Plotas={}, Aukštas={}, Aukštų={}, Kaina={} \n'.format(
        timestamp, rajonas, gatve, kambariai, plotas, aukstas, aukstu, prediction))
    data.close()


@app.route("/", methods=['GET', 'POST'])
def hello():
    form = ReusableForm(request.form)
    if request.method == 'POST':
        rajonas = request.form['rajonas']
        kambariai = request.form['kambariai']
        plotas = request.form['plotas']
        aukstas = request.form['aukstas']
        aukstu = request.form['aukstu']
        vardas = request.form['vardas']
        email = request.form['email']

        dummies = []
        for i in rajonai_form:
            if i == rajonas:
                i = 1
                dummies.append(i)
            else:
                i = 0
                dummies.append(i)

        data = [kambariai, plotas, aukstas, aukstu]
        data = list(map(int, data))
        data = data + dummies
        prediction = form_model.predict(
            [data])[0]

        if form.validate():
            log_form(rajonas, kambariai, plotas, aukstas,
                     aukstu, vardas, email, prediction)
            flash('Paskaičiuota preliminari būsto kaina: ' +
                  str(int(prediction)) + 'eur')
        else:
            flash('Visi laukai yra privalomi!')

    return render_template('index.html', form=form)


@app.route('/api', methods=['POST'])
def api_json():
    req_data = request.get_json()

    rajonas = req_data['rajonas']
    gatve = req_data['gatve']
    kambariai = req_data['kambariai']
    plotas = req_data['plotas']
    aukstas = req_data['aukstas']
    aukstu = req_data['aukstu']

    dummies = []
    for i in rajonai_json:
        if i == rajonas:
            i = 1
            dummies.append(i)
        else:
            i = 0
            dummies.append(i)

    g = gatves.loc[gatves['Gatve'] == gatve]
    g = g.drop('Gatve', axis=1).values.tolist()[0]

    data = [kambariai, plotas, aukstas, aukstu]
    data = list(map(int, data))
    data = data + g + dummies
    prediction = json_model.predict([data])[0]

    log_json(rajonas, gatve, kambariai, plotas, aukstas, aukstu, prediction)

    return jsonify({'prediction': prediction})


if __name__ == "__main__":
    app.run()
