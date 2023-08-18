from flask import Flask, render_template
from flask_mysqldb import MySQL

import flask
import MySQLdb.cursors
import json
import decimal_encoder as de

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'dbcontainer'
app.config['MYSQL_USER'] = 'example_user'
app.config['MYSQL_PASSWORD'] = 'mysql'
app.config['MYSQL_DB'] = 'example'
app.config['MYSQL_PORT'] = 3306

mysql = MySQL(app)

@app.route('/', methods=['GET'])
@app.route('/students/list', methods=['GET'])
def student_list_json():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM student')
    data = cursor.fetchall()
    return render_template('index.html', studends=data)

@app.route('/students/create', methods=['GET'])
def view_create_student():
    return render_template('create_students.html')

@app.route('/student/update/<int:id>', methods=['GET'])
def view_update_students(id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM student WHERE id=%i" % id)
    data = cursor.fetchone()
    return render_template('update_student.html', student=data)

@app.route('/students', methods=['GET'])
def get_students_list():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM student')
    data = cursor.fetchall()
    resp = flask.Response(json.dumps(data, cls=de.DecimalEncoder))
    resp.headers['Content-Type'] = 'application/json'
    return resp

@app.route('/students', methods=['POST'])
def add_and_update_student():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    data = request.form

    if 'id' in data:
        cursor.execute("UPDATE student SET first_name='%s', last_name='%s', city='%s', semester='%s' WHERE id=%i" % 
                   (data['first_name'], data['last_name'], data['city'], data['semester']))
    else:
        cursor.execute("INSERT INTO student (first_name, last_name, city, semester) VALUES ('%s', '%s', '%s', '%s')" % 
                    (data['first_name'], data['last_name'], data['city'], data['semester']))

    mysql.connection.commit()
    resp = flask.Response(json.dumps({'result': 'ok'}))
    resp.headers['Content-Type'] = 'application/json'
    return redirect(url_for('student_list_json'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)

