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


@app.route('/user/regist', methods=['post'])
def regist():
    json_data = flask.request.json
    if json_data == None:
        result = {"pesan": "Not available"}
        return jsonify(result)
    else:
        nama = json_data['nama']
        nik = json_data['nik']
        card_uid = json_data['card_uid']
        id_saldo = card_uid
        db = mysql.connector.connect(host="localhost",
                                     user="root",
                                     password="",
                                     database="rfidattendance")
        check_Nik = check_nik(nik)
        check_Id_saldo = check_id_saldo(card_uid)
        if check_Nik == 1 and check_Id_saldo == 1:
            result = {"pesan": "User sudah terdaftar"}
            return jsonify(result)
        else:
            cursor = db.cursor()
            cursor.execute(
                "INSERT INTO `users`(`nama`, `nik`, `card_uid`, `id_saldo`) VALUES(%s,%s,%s,%s)",
                (nama, nik, card_uid, id_saldo))
            cursor.execute(
                "INSERT INTO `saldo`(`id_saldo`, `beras`, `sayur`, `lauk`) VALUES(%s,%s,%s,%s)",
                (card_uid, 2, 1, 1))
            db.commit()
            result = {"pesan": "Daftar berhasil"}
            return jsonify(result)


def check_nik(a):
    db = mysql.connector.connect(host="localhost",
                                 user="root",
                                 password="",
                                 database="rfidattendance")
    cursor = db.cursor()
    cursor.execute("SELECT nik FROM users where nik=%s", (a, ))
    a = cursor.fetchone()
    if a == None:
        return 0
    else:
        return 1


def check_id_saldo(b):
    db = mysql.connector.connect(host="localhost",
                                 user="root",
                                 password="",
                                 database="rfidattendance")
    cursor = db.cursor()
    cursor.execute("SELECT id_saldo FROM saldo where id_saldo=%s", (b, ))
    a = cursor.fetchone()
    if a == None:
        return 0
    else:
        return 1


if __name__ == "__main__":
    #serve(app, host="0.0.0.0", port=7000)
    app.run(port=7000, debug=True)