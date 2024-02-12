from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3
                                                                                                                                       
app = Flask(__name__)                                                                                                                  
                                                                                                                                       
@app.route('/')
def hello_world():
    return render_template('hello.html') #Comm1
@app.route("/contact/")
def MaPremiereAPI():
    return render_template("contact.html")
@app.route('/paris/')
def meteo():
    response = urlopen('https://api.openweathermap.org/data/2.5/forecast/daily?q=Paris,fr&cnt=16&appid=bd5e378503939ddaee76f12ad7a97608')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('temp', {}).get('day') - 273.15 # Conversion de Kelvin en °c 
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)
@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")
@app.route("/histogramme/")
def monhistogramme():
    return render_template("histogramme.html")
@app.route('/commits/')
def commits():
    # Appel à l'API GitHub pour récupérer les données sur les commits
    response = requests.get('https://github.com/shelton1007/5MCSI_Metriques')
    commits_data = response.json()

    # Analyse des données pour compter les commits par minute
    commits_per_minute = {}
    for commit in commits_data:
        date_string = commit['commit']['author']['date']
        minute = date_string[14:16]  # Extraire les minutes de la date
        commits_per_minute[minute] = commits_per_minute.get(minute, 0) + 1

    # Création de listes de minutes et de quantités de commits pour le graphique
    minutes = list(commits_per_minute.keys())
    commits_count = list(commits_per_minute.values())

    return render_template('commits.html', minutes=minutes, commits_count=commits_count)

if __name__ == "__main__":
  app.run(debug=True)
