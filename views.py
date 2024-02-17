from flask import Flask, render_template, request
from wsgi import app, df
from modules import count_cosine

@app.route('/', methods=['POST', 'GET'])
def characters():
    headers = ['Name']
    search_value = str(request.form.get('search'))
    if search_value == "None":
        search_value = ''
    data_len = str(request.form.get('data_len'))
    if data_len == "None":
        data_len = ''
    return render_template("characters.html", df=df, headers=headers, search_value=search_value)


@app.route('/<int:id>', methods=['POST', 'GET'])
def similarity(id):
    character = df.loc[id]
    df_similarity = count_cosine(df, character)
    return render_template("similarity.html", df_similarity=df_similarity, df=df, id=id)

