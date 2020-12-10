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


@app.route('/user/ambil', methods=['POST'])
def ambil():
    json_data = flask.request.json
    if json_data == None:
        result = {
            "beras": "Not available",
            "sayur": "Not available",
            "lauk": "Not available"
        }
        return jsonify(result)
    else:
        nama = json_data['nama']
        card_uid = json_data['card_uid']
        cek = check_user(nama, card_uid)
        if cek == 1:
            saldo = get_saldo(card_uid)
            if saldo == 0:
                result = {
                    "beras": "Not available user",
                    "sayur": "Not available user",
                    "lauk": "Not available user"
                }
                return jsonify(result)
            else:
                result = {
                    "beras": saldo[0],
                    "sayur": saldo[1],
                    "lauk": saldo[2]
                }
                return jsonify(result)
        else:
            result = {
                "beras": "Not available user",
                "sayur": "Not available user",
                "lauk": "Not available user"
            }
            return jsonify(result)


@app.route('/user/ambil/confirm', methods=['POST'])
def confirm():
    json_data = flask.request.json
    if json_data == None:
        result = {"pesan": "Not Available"}
        return jsonify(result)
    else:
        nama = json_data['nama']
        id_saldo = json_data['card_uid']
        beras = json_data['beras']
        sayur = json_data['sayur']
        lauk = json_data['lauk']
        cek = check_user(nama, id_saldo)
        if cek == 0:
            result = {"pesan": "user not available"}
            return jsonify(result)
        else:
            db = mysql.connector.connect(host="localhost",
                                         user="root",
                                         password="",
                                         database="rfidattendance")
            cursor = db.cursor()
            cursor.execute(
                "UPDATE `saldo` SET `beras`=%s,`sayur`=%s,`lauk`=%s WHERE `id_saldo` = %s",
                (beras, sayur, lauk, id_saldo))
            db.commit()
            result = {"pesan": "berhasil"}
            return jsonify(result)


@app.route("/user/logs", methods=['POST'])
def logs():
    json_data = flask.request.json
    if json_data == None:
        result = {"pesan": "Not Available"}
        return jsonify(result)
    else:
        nama = json_data['nama']
        card_uid = json_data['card_uid']
        nik = get_nik(nama, card_uid)
        time = datetime.datetime.now()
        tanggal = time.strftime("%d-%m-%Y")
        jam = time.strftime("%H:%M:%S")
        waktu = tanggal + " " + jam
        db = mysql.connector.connect(host="localhost",
                                     user="root",
                                     password="",
                                     database="rfidattendance")
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO `users_logs`(`nama`, `nik`, `card_uid`, `waktu`) VALUES (%s,%s,%s,%s)",
            (nama, nik, card_uid, waktu))
        db.commit()
        result = {"pesan": "Tercatat"}
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


def get_nik(a, b):
    db = mysql.connector.connect(host="localhost",
                                 user="root",
                                 password="",
                                 database="rfidattendance")
    cursor = db.cursor()
    cursor.execute("SELECT nik from users where nama=%s and card_uid=%s",
                   (a, b))
    a = cursor.fetchone()
    if a == None:
        return None
    else:
        return a[0]


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


def check_user(a, b):
    db = mysql.connector.connect(host="localhost",
                                 user="root",
                                 password="",
                                 database="rfidattendance")
    cursor = db.cursor()
    cursor.execute(
        "SELECT card_uid FROM users where nama = %s and card_uid = %s", (a, b))
    a = cursor.fetchone()
    if a == None:
        return 0
    else:
        return 1


def get_saldo(a):
    db = mysql.connector.connect(host="localhost",
                                 user="root",
                                 password="",
                                 database="rfidattendance")
    cursor = db.cursor()
    cursor.execute("SELECT beras,sayur,lauk where id_saldo = %s", (a, ))
    a = cursor.fetchone()
    if a == None:
        return 0
    else:
        return a


if __name__ == "__main__":
    #serve(app, host="0.0.0.0", port=7000)
    app.run(port=7000, debug=True)