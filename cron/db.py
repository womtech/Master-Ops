#!/usr/bin/python
# -*- coding: utf-8 -*-
import mysql.connector
import psycopg2
import datetime
from mysql.connector import Error


def connect():
    """ Connect to MySQL database """

    try:
        conn = mysql.connector.connect(host='localhost', database='qc',user='dev', password='d3v@100%')
        con = psycopg2.connect(database='mops', user='mops',password='P@$$w0rd100%',host='127.0.0.1', port='5432')
        if conn.is_connected():
            print ('Connected to MySQL database')
            mysqlcursor = conn.cursor()
            postgresqlcursor = con.cursor()
            today = datetime.datetime.now().date()
            todaydate = repr(str(today))
            mysqlcursor.execute('SELECT * FROM bucket_videos where created_on='+todaydate+'')
            myresult = mysqlcursor.fetchall()
            print(today)
            for x in myresult:
                print(x[1])
                postgresqlcursor.execute('SELECT * FROM bucket_videos where created_on='+todaydate+'')
            
            print ('Opened database successfully')
    except Error as e:
        print(e)
    finally:

        conn.close()


if __name__ == '__main__':
    connect()
