import subprocess
import json
import mysql.connector

from settings import *

con=mysql.connector.connect(user=MYSQL_USER,
                            password=MYSQL_PASSWORD,
                            database=MYSQL_DATABASE)
cur=con.cursor()

out = subprocess.check_output(['bitcoin-cli', 'getinfo'])
parsed = json.loads(out)
insertstmt=("insert into proc (created, metric, value) values (now(), '%s', '%s')" % ('blocks_bitcoind', parsed['blocks']))
cur.execute(insertstmt)
insertstmt=("insert into proc (created, metric, value) values (now(), '%s', '%s')" % ('difficulty_bitcoind', parsed['difficulty']))
cur.execute(insertstmt)

con.commit()
con.close()
