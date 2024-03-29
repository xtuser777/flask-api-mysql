from flask import Flask, make_response, jsonify, request
from mysql.connector import (connection, errorcode, Error)

def get_connection():
    try:
        conn = connection.MySQLConnection(
            host='localhost',
            user='root',
            password='root',
            database='flask_api'
        )
    except Error as err:
        conn = None
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)

    return conn

app = Flask(__name__)

@app.route('/cars', methods=['GET'])
def index():
    conn = get_connection()
    if conn and conn.is_connected():
        cars = list()

        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM cars")
            carsdb = cursor.fetchall()
            for car in carsdb:
                cars.append(
                    {
                        'id': car[0],
                        'brand': car[1],
                        'model': car[2],
                        'year': car[3]
                    }
                )
            cursor.close()
        except Error as err:
            print(err)
            return make_response(jsonify(err.msg), 500)
        else:
            conn.close()

        return make_response(jsonify(cars), 200)
    else:
        return make_response(jsonify(message='Erro de conexão ao banco.'), 500)

@app.route('/cars/<int:id>', methods=['GET'])
def show(id: int):
    conn = get_connection()
    if conn and conn.is_connected():
        car = None

        try:
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM `cars` WHERE `id` = {id}")
            carsdb = cursor.fetchone()
            car = {
                'id': carsdb[0],
                'brand': carsdb[1],
                'model': carsdb[2],
                'year': carsdb[3]
            }
            cursor.close()
        except Error as err:
            print(err)
            return make_response(jsonify(err.msg), 500)
        else:
            conn.close()

        return make_response(jsonify(car), 200)
    else:
        return make_response(jsonify(message='Erro de conexão ao banco.'), 500)

@app.route('/cars', methods=['POST'])
def create():
    conn = get_connection()
    if conn and conn.is_connected():
        car = None

        try:
            car = request.json
            cursor = conn.cursor()
            query = "INSERT INTO `cars` (`brand`,`model`,`year`) VALUES (%(brand)s,%(model)s,%(year)s)"
            cursor.execute(query, car)
            conn.commit()
            cursor.close()
        except Error as err:
            print(err)
            return make_response(jsonify(err.msg), 500)
        else:
            conn.close()

        return make_response(jsonify(car), 201)
    else:
        return make_response(jsonify(message='Erro de conexão ao banco.'), 500)

@app.route('/cars/<int:id>', methods=['PUT'])
def update(id: int):
    conn = get_connection()
    if conn and conn.is_connected():
        car = None

        try:
            car = request.json
            car['id'] = id
            cursor = conn.cursor()
            query = "UPDATE `cars` SET `brand` = %(brand)s, `model` = %(model)s, `year` = %(year)s WHERE `id` = %(id)s"
            cursor.execute(query, car)
            conn.commit()
            cursor.close()
        except Error as err:
            print(err)
            return make_response(jsonify(err.msg), 500)
        else:
            conn.close()

        return make_response(jsonify(car), 200)
    else:
        return make_response(jsonify(message='Erro de conexão ao banco.'), 500)

@app.route('/cars/<int:id>', methods=['DELETE'])
def delete(id: int):
    conn = get_connection()
    if conn and conn.is_connected():
        try:
            cursor = conn.cursor()
            query = "DELETE FROM `cars` WHERE `id` = %(id)s"
            params = { 'id': id }
            cursor.execute(query, params)
            conn.commit()
            cursor.close()
        except Error as err:
            print(err)
            return make_response(jsonify(err.msg), 500)
        else:
            conn.close()

        return make_response(jsonify(None), 204)
    else:
        return make_response(jsonify(message='Erro de conexão ao banco.'), 500)
    
app.run()