# bitstats

Bitcoin and cryptocurrency statistics developed for http://bitcoinexchangerate.org

# Setup

## Pre-requisites
 * GNU/Linux with Webmin installed.
 * Bandwidth monitoring enabled in Webmin.
 * Mysql database
 * sudo apt-get install python-mysql.connector 
 
## Installation
1. Create a user and make /var/log/bandwidth readable by that user.
2. Copy default_settings.py to settings.py and set your database credentials.
3. Run bandwidth monitor script in background with `python tail_bandwidth.py &`

