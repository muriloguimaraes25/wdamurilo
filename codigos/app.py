from flask import Flask, jsonify
import pandas as pd
import json

app = Flask(__name__)

@app.route('/')
def oi():
    return 'A AP2 está no ar'

@app.route('/dados')
def carregardados1():
    df = pd.read_csv('../bases_originais/base_bruta.csv', sep=';', encoding='utf=8')
    return jsonify(df.to_json())

# ___________________ CRIANDO OUTRA ROTA PARA OS DADOS TRATADOS ___________________ #

@app.route('/dadostratados')
def carregardados2():
    df = pd.read_csv('../bases_tratadas/base_tratada.csv', sep=';', encoding='utf=8')
    return jsonify(df.to_json())

if __name__ == '__main__':
    app.run(debug=True)