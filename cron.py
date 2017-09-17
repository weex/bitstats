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

con.commit()
con.close()
