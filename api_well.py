import flask
import mysql.connector
from flask import Flask, jsonify, request
import uuid
import base64
import hashlib
import json
import datetime
from datetime import date
import calendar
from waitress import serve
app = Flask(__name__)


@app.route('/user/ambil', methods=['post'])
def regist():
    json_data = flask.request.json
    if json_data == None:
        result = {"pesan": "Not available"}
        return jsonify(result)
    else:
        id = json_data['id']
        nama = json_data['nama']
        nik = json_data['nik']
        beras = json_data['beras']
        sayur = json_data['sayur']
        lauk = json_data['lauk']
        db = mysql.connector.connect(host="localhost",
                                     user="root",
                                     password="",
                                     database="rfidattendance")
        check = check_id(id)
        if check == 0:
            result = {"pesan": "User belum terdaftar"}
            return jsonify(result)
        else:
            cursor = db.cursor()
            cursor.execute(
                "INSERT INTO `users`(`id`, `nama`, `nik`, `beras`, `sayur`, `lauk`) VALUES (%s,%s,%s,%s,%s,%s)",
                (id, nama, nik, beras, sayur, lauk))
            db.commit()
            result = {"message": "input berhasil"}
            return jsonify(result)


def check_id(a):
    db = mysql.connector.connect(host="localhost",
                                 user="root",
                                 password="",
                                 database="rfidattendance")
    cursor = db.cursor()
    cursor.execute("SELECT id FROM admin where id=%s", (a, ))
    a = cursor.fetchone()
    if a == None:
        return 0
    else:
        return 1


if __name__ == "__main__":
    # serve(app, host="0.0.0.0", port=7000)
    app.run(port=7000, debug=True)