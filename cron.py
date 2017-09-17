import subprocess
import mysql.connector

from settings import *

con=mysql.connector.connect(user=MYSQL_USER,
                            password=MYSQL_PASSWORD,
                            database=MYSQL_DATABASE)
cur=con.cursor()

dirs = {'/home/dsterry/.ethereum': 'geth',
        '/home/dsterry/.bitcoin': 'bitcoind'}

for d in dirs:
    out = subprocess.check_output(['du', '-s', d])
    du = out.strip().split('\t')[0]
    
    insertstmt=("insert into disk (created, metric, value) values (now(), '%s', '%s')" % ('disk_'+dirs[d], du))
    cur.execute(insertstmt)

    out = subprocess.check_output(['ps', '-C', dirs[d], '-o', '%cpu,%mem'])
    out = out.split('\n')[1]
    cpu = out.split(' ')[0]
    mem = out.split(' ')[-1]
    insertstmt=("insert into proc (created, metric, value) values (now(), '%s', '%s')" % ('cpu_'+dirs[d], cpu))
    cur.execute(insertstmt)
    insertstmt=("insert into proc (created, metric, value) values (now(), '%s', '%s')" % ('mem_'+dirs[d], mem))
    cur.execute(insertstmt)

con.commit()
con.close()
