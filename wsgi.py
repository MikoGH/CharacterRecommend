from flask import Flask, render_template
import pandas as pd

app = Flask(__name__, static_folder="static", static_url_path='')
app.config['SECRET_KEY'] = 'secret_key'

df = pd.read_csv('Anime_Traits_Wide.csv', nrows=4000) # 25000
# df['Tags'] = df['Tags'].str.split('|')

from views import *

if __name__ == "__main__":
    app.run(debug=True)
    