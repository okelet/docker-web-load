import os
import socket
import time
from datetime import datetime
from multiprocessing import cpu_count, Pipe, Process
from typing import Optional

from flask import Flask, Response

app = Flask(__name__)

##########################################################################################
# Borrowed from https://github.com/shichao-an/pystress/blob/master/pystress.py
##########################################################################################

FIB_N = 100


def loop(conn):
    proc_info = os.getpid()
    conn.send(proc_info)
    conn.close()
    while True:
        fib(FIB_N)


def fib(n):
    if n < 2:
        return 1
    else:
        return fib(n - 1) + fib(n - 2)


def cpu_load(exec_time: Optional[int] = None, proc_num: Optional[int] = None):

    if exec_time is None:
        exec_time = 5

    if proc_num is None:
        proc_num = cpu_count()

    procs = []
    conns = []
    for i in range(proc_num):
        parent_conn, child_conn = Pipe()
        p = Process(target=loop, args=(child_conn,))
        p.start()
        procs.append(p)
        conns.append(parent_conn)

    for conn in conns:
        try:
            conn.recv()
        except EOFError:
            continue

    time.sleep(exec_time)

    for p in procs:
        p.terminate()

##########################################################################################
##########################################################################################


@app.route("/")
def home():
    return Response(
        "Welcome from " + socket.gethostname() + "\nEnvironment variable VAR_1 is " + os.getenv("VAR_1", "__NO_DATA__") + "\n",
        mimetype='text/plain'
    )


@app.route('/env')
def env():
    data = "Environment:\n"
    for item, value in os.environ.items():
        data += f"{item} => {value}\n"
    return Response(
        data,
        mimetype='text/plain'
    )


@app.route("/load")
def load():
    start_dt = datetime.utcnow()
    cpu_load()
    end_dt = datetime.utcnow()
    return Response(
        f"Load generated; start: {start_dt}, end: {end_dt}\n",
        mimetype='text/plain'
    )


@app.route("/healthcheck")
def healthcheck():
    return Response(
        "OK\n",
        mimetype='text/plain'
    )
