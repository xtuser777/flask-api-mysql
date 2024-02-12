from flask import Flask, make_response, jsonify, request
from mysql.connector import (connection)

def get_connection():
    conn = connection.MySQLConnection(
        host='localhost',
        user='root',
        password='root',
        database='flask_api'
    )

    return conn

app = Flask(__name__)

@app.route('/cars', methods=['GET'])
def index():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cars")
    carsdb = cursor.fetchall()
    cars = list()
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
    conn.close()

    return make_response(jsonify(cars), 200)

@app.route('/cars/<int:id>', methods=['GET'])
def show(id: int):
    conn = get_connection()
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
    conn.close()

    return make_response(jsonify(car), 200)



@app.route('/cars', methods=['POST'])
def create():
    conn = get_connection()
    car = request.json
    cursor = conn.cursor()
    cursor.execute(f"INSERT INTO `cars` (`brand`,`model`,`year`) VALUES ('{car['brand']}','{car['model']}',{car['year']})")
    conn.commit()
    cursor.close()
    conn.close()

    return make_response(jsonify(car), 201)

@app.route('/cars/<int:id>', methods=['PUT'])
def update(id: int):
    conn = get_connection()
    car = request.json
    cursor = conn.cursor()
    cursor.execute(f"UPDATE `cars` SET `brand` = '{car['brand']}',`model` = '{car['model']}',`year` = {car['year']} WHERE `id` = {id}")
    conn.commit()
    cursor.close()
    conn.close()

    return make_response(jsonify(car), 200)

@app.route('/cars/<int:id>', methods=['DELETE'])
def delete(id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM `cars` WHERE `id` = {id}")
    conn.commit()
    cursor.close()
    conn.close()

    return make_response(jsonify(), 204)

app.run()