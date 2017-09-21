#!/usr/bin/env python
import time
import subprocess
import select
import mysql.connector

from settings import *

con=mysql.connector.connect(user=MYSQL_USER,
                            password=MYSQL_PASSWORD,
                            database=MYSQL_DATABASE)
cur=con.cursor()

filename = '/var/log/bandwidth'
seconds = INTERVAL
ports = ['30303', '8333']

f = subprocess.Popen(['tail','-F',filename],\
        stdout=subprocess.PIPE,stderr=subprocess.PIPE)
proc = select.poll()
proc.register(f.stdout)


def process():
    start = time.time()
    kBps = {}
    for p in ports:
        kBps[p] = {}
        kBps[p]['tot'] = 0
        kBps[p]['in'] = 0
        kBps[p]['out'] = 0
    while True:
        if proc.poll(1):
            data = parse(f.stdout.readline())
            if not data or 'LEN' not in data:
                continue
            Bytes = int(data['LEN'])
            for p in ports:
                if data.get('SPT', '') == p or data.get('DPT', '') == p:
                    kBps[p]['tot'] += Bytes
                    if data.get('DIR', '') == 'IN':
                        kBps[p]['in'] += Bytes
                    else:
                        kBps[p]['out'] += Bytes
            if time.time() - start > seconds:
                print kBps
                for k in kBps:
                    for metric in kBps[k]:
                        insertstmt=("insert into bandwidth (created, metric, value) values (now(), '%s', '%s')" % (k+'_'+metric, kBps[k][metric]/float(seconds)))
                        cur.execute(insertstmt)
                    con.commit()
                for p in ports:
                    kBps[p]['tot'] = 0
                    kBps[p]['in'] = 0
                    kBps[p]['out'] = 0
                start = time.time()
    con.close()

#  Sep 17 03:42:01 usloft5264 kernel: [347006.315335] BANDWIDTH_IN:IN=eth0 OUT= MAC=84:34:97:11:3b:bc:00:24:38:a4:b8:00:08:00 SRC=163.44.174.122 DST=209.239.115.243 LEN=52 TOS=0x00 PREC=0x00 TTL=50 ID=40038 DF PROTO=TCP SPT=53482 DPT=30303 WINDOW=10077 RES=0x00 ACK URGP=0

def parse(line):
    _time = line[:15]
    _data = line[51:]

    fields = _data.split(' ')
    out = {}
    for f in fields:
        if ':' in f:
            f = f.replace('BANDWIDTH_IN:IN','IN')
            f = f.replace('BANDWIDTH_OUT:IN','IN')

        if '=' in f:
            key, value = f.split('=')
            out[key] = value
            if key == 'IN':
                if value:
                    out['DIR'] = 'IN'
                else:
                    out['DIR'] = 'OUT'
    return out


if __name__ == "__main__":
    process()

