import os

import statsmodels.tools
from flask import Flask, flash, request, redirect, render_template
from werkzeug.utils import secure_filename
import analysis
from os.path import exists
import matplotlib.pyplot as plt
import pandas as pd
from sklearn import linear_model
from sklearn.model_selection import train_test_split
import plotcreator
from statsmodels.api import OLS
import statsmodels.api as sm
#flask configuration
UPLOAD_FOLDER = 'uploaded_files'
ALLOWED_EXTENSIONS = {'csv'}
app = Flask(__name__)
app.secret_key = "key-secret"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename: str)->str:
    '''
        checks if uploaded to server file has allowed format (csv)
    '''
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def read_file_to_pandas(filename: str)-> pd.DataFrame:
    '''
    reads file from uploaded_files and converts it to dataframe
    '''
    df = pd.read_csv('uploaded_files/' + filename)
    return df

@app.route('/', methods=['GET', 'POST'])
def upload_csv():
    # https://flask.palletsprojects.com/en/2.1.x/patterns/fileuploads/
    # uploading file, source: flask documentation
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files.get('file')
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect('/imported-data/{0}'.format(filename))
    return render_template("index.html")

@app.route('/imported-data/<filename>')
def uploaded_file(filename):
    file_exists = exists('uploaded_files/' + filename)
    if file_exists:
        df = read_file_to_pandas(filename)
        # returning sample of date(1st 5 records)
        return render_template("overview.html", sample=df.head().to_html(), file=filename)
    else:
        return "there is no such a file"

@app.route('/static/statistics/<filename>')
def generate_stats(filename):
    # generating statistics sonly for a numerical data and returning it in table
    file_exists = exists('uploaded_files/' + filename)
    if file_exists == True:
        df = read_file_to_pandas(filename)
        data = analysis.ImportedFile(df)
        size_string = data.return_size()
        statistics = data.return_statistics().to_html()
        missing_values = data.return_missing_percentage().to_html()
        return render_template("statistics.html", sample=df.head().to_html(), stats=statistics,
                               missing=missing_values, size=size_string)
    else:
        return render_template("missing.html")

@app.route('/static/twodimensionplot/<filename>', methods=['GET', 'POST'])
def twodimensionplot(filename):
    # check if file exists
    file_exists = exists('uploaded_files/' + filename)
    df = read_file_to_pandas(filename)
    if request.method == 'GET':
        cols = list(df.columns)
        options = ['linear','scatter','bar']
        return render_template('collumns.html', cols=cols,graphoptions=options)
    if request.method == 'POST':
        select_first = str(request.form.get('comp_select'))
        select_second = str(request.form.get('comp_select2'))
        select_third = str(request.form.get('comp_select3'))
        x = df[select_first]
        y = df[select_second]
        filename = filename[:-4].lower()
        image_id = filename+select_first+select_second+select_third
        image_id = image_id.replace(" ", "")
        plot = plotcreator.Plotcreator()
        if select_third=="linear":
            plot.linear_plot(x,y,image_id)
        if select_third=="scatter":
            plot.scatter(x,y,image_id)
        if select_third=="bar":
            plot.barplot(x, y, image_id)
        return render_template("graph.html",image_data = "/static/{}.png".format(image_id))

@app.route('/static/twodimensionreggresion/<filename>', methods=['GET', 'POST'])
def twodimensionreggresion(filename):
    # check if file exists
    file_exists = exists('uploaded_files/' + filename)
    df = read_file_to_pandas(filename)
    if request.method == 'GET':
        cols = list(df.columns)
        options = ['linear-regression','logistic-regression(beta)','multi-task Lasso(beta)','bayesian Regression(beta)',
                   'stochastic Gradient Descent(beta)','robustness regression(beta)']
        return render_template('collumns.html', cols=cols,graphoptions=options)
    if request.method == 'POST':
        select_first = str(request.form.get('comp_select'))
        select_second = str(request.form.get('comp_select2'))
        select_third = str(request.form.get('comp_select3'))
        x = df[select_first]
        y = df[select_second]
        filename = filename[:-4].lower()
        image_id = filename+select_first+select_second+select_third
        image_id = image_id.replace(" ", "")
        x = x.values
        y = y.values
        x = x.reshape(len(x), 1)
        y = y.reshape(len(y), 1)

        if select_third == 'linear-regression':
            reg = linear_model.LinearRegression()
            reg.fit(x, y)
            y_pred = reg.predict(x)
            plt.rcParams["figure.figsize"] = (15, 15)
            plt.figure(facecolor='#082032')
            ax = plt.axes()
            ax.set_facecolor("yellow")
            ax.tick_params(axis='x', colors='white')
            ax.tick_params(axis='y', colors='white')
            plt.scatter(x, y, color="black")
            plt.plot(x, y_pred, color="blue", linewidth=3)
            plt.savefig('static/{}.png'.format(image_id))
            x = df[select_first]
            y = df[select_second]
            x = sm.add_constant(x)
            summ = (OLS(y,x).fit().summary())
            t1=summ.tables[0].as_html()
            t2=summ.tables[1].as_html()
            t3=summ.tables[2].as_html()
            return render_template("graph.html", image_data="/static/{}.png".format(image_id),
                                   first_table =t1,
                                   second_table = t2,
                                   third_table = t3)
        else:
            return render_template("development.html")
if __name__ == "__main__":
    app.debug = True
    app.run()
