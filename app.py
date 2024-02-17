# -*- coding: utf-8 -*-
"""
Created on Sun Feb 11 00:49:12 2024

@author: crist
"""

from flask import Flask, render_template, request, send_file
import pandas as pd
#import sqlite3 
import pypyodbc as odbc 
import sys


app = Flask(__name__)
#app.config['UPLOAD_FOLDER'] = 'C:\\Users\\crist\\OneDrive\\Escritorio\\Proyecto  BBDD'

def create_connection(db_file):
    conn = None
    try:
        conn = odbc.connect(db_file)
        return conn
    except odbc.Error as e:
        print(e)
    return conn

def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except odbc.Error as e: 
        print(e)
 
def insert_data(conn, data):
    sql = ''' INSERT INTO Persons(PersonID,FirstName,LastName,Address,City)
              VALUES(?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, data)
    conn.commit() 
    return #cur.lastrowid

def verificar_credenciales(username, password):
    # Conexión a la base de datos de Azure SQL
    conn=odbc.connect('Driver={ODBC Driver 18 for SQL Server};Server=server-web-submit.database.windows.net;Database=BD_web_submit;Uid=Parro;Pwd=Callelepanto12')
    # Crear un cursor para ejecutar consultas SQL
    cursor = conn.cursor()

    # Consulta SQL para verificar las credenciales
    #EL FALLO ESTÁ AQUÍ.
    query = "SELECT COUNT(*) FROM Usuarios WHERE Usuario=? AND Contrasena=?"
    
    cursor.execute(query, (username, password))

    # Obtener el resultado de la consulta
    count = cursor.fetchone()[0]
    # Cerrar la conexión y el cursor
    cursor.close()
    conn.close()
    
    # Si el recuento es mayor que 0, las credenciales son válidas
    return count > 0


@app.route('/')
def index():
    return render_template('user.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':        
        username = request.form['username']
        password = request.form['password']
        # Verificar las credenciales del usuario en la base de datos
        if verificar_credenciales(username, password):
            # Si las credenciales son válidas, redireccionar a otra página
            return render_template('index.html')
        else:
            return'Credenciales incorrectas'
    else:
        return 'aaa'
    #return render_template('login.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file:
        try:
            conn =odbc.connect('Driver={ODBC Driver 18 for SQL Server};Server=server-web-submit.database.windows.net;Database=BD_web_submit;Uid=Parro;Pwd=Callelepanto12')
            df = pd.read_excel(file)           
            
            # Guardar cada fila del DataFrame en la base de datos
            for _, row in df.iterrows():
                data = (row['PersonID'], row['FirstName'], row['LastName'],row['Address'],row['City'])  # Ajusta los nombres de las columnas según tu archivo Excel
                insert_data(conn, data)            
                #conn.close()
            return 'File uploaded successfully and data saved to database'
            
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            return str(e),str(exc_type)
            #return render_template('index.html', error_message=str(e))
@app.route('/download_excel')
def download_excel():
    # Consulta los datos de la base de datos
    conn =odbc.connect('Driver={ODBC Driver 18 for SQL Server};Server=server-web-submit.database.windows.net;Database=BD_web_submit;Uid=Parro;Pwd=Callelepanto12')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Persons")
    rows = cursor.fetchall()

    # Crea un DataFrame de pandas con los datos
    df = pd.DataFrame(rows, columns=[column[0] for column in cursor.description])

    # Guarda el DataFrame en un archivo Excel
    excel_file = 'data.xlsx'
    df.to_excel(excel_file, index=False)

    # Envia el archivo Excel como respuesta para descargarlo
    return send_file(excel_file, as_attachment=True)
if __name__ == '__main__':
    #from waitress import serve
    #serve(app, host="0.0.0.0", port=8080)
    app.run(debug=False)