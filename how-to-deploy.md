# linux-server-configuration
fsnd - install and configure a server, secure from attack vectors, manage database, and deploy web application.

## Amazon Lightsail Instance
1. IP address: 13.114.200.91
2. Webapp url: http://13.114.200.91/catalog/
3. SSH to instance as grader: `ssh grader@13.114.200.91 -p 2200`

## Prerequirement
1. python: python2 python-pip python-flask
2. apache: apache2 libapache2-mod-wsgi
3. database: sqlite3 python-sqlalchemy
4. python packages: setuptools bleach oauth2client requests httplib2 redis passlib pyth itsdangerou flask-httpauth Flask-Login Github-Flask
5. webapp: [github-catalog](https://github.com/yogykwan/github-catalog)

## Configuration

### User Management
1. create sudo user grader
```
sudo adduser grader
sudo echo 'grader ALL=(ALL) NOPASSWD:ALL' | tee /etc/sudoers.d/grader
```

2. generate ssh key pairs from local machine
```
ssh-keygen # save to ~/.ssh/udacity_linux
chmod 600 ~/.ssh/udacity_linux
ssh-add ~/.ssh/udacity_linux
```

3. save public key to /home/grader/.ssh/authorized_keys on aws
```
sudo chmod 700 /home/grader/.ssh
sudo chmod 644 /home/grader/.ssh/authorized_keys
```

4. configure ssh in /etc/ssh/sshd_config
```
Port 2200 # change default ssh port
PermitRootLogin no # disallow ssh as root
PasswordAuthentication no # enforce key-based ssh authentication
```

### Security
1. update packages
```
sudo apt-get update && apt-get upgrade
```

2. configure ufw
```
sudo ufw default deny incoming
sudo ufw default deny outgoing
sudo ufw allow www
sudo ufw allow ntp
sudo utf allow 2200/tcp
sudo utf enable
```

### Application Functionality
1. clone webapp repo from github
```
sudo mkdir /var/www/catalog/
sudo chown www-data:www-data /var/www/catalog
sudo -u git clone https://github.com/yogykwan/github-catalog.git
sudo cp -R github-catalog/vagrant/catalog /var/www/catalog/
sudo python /var/www/catalog/catalog/__init__.py # run flask app on port 5000
```

2. prepare database (sqlite3)
```
sudo python /var/www/catalog/catalog/database_create.py
sudo python /var/www/catalog/catalog/database_inject.py
```

3. create /var/www/catalog/catalog.wsgi
```
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/catalog")
from catalog import app as application
from catalog.database_setup import create_db
from catalog.database_inject import inject_db
create_db()
inject_db()
```

4. create virtual host in /etc/apache2/sites-available/catalog.conf to respond port 80 with proxy 5000
```
<VirtualHost *:80>
ServerName localhost
ProxyRequests Off
ProxyPass / http://localhost:5000/
ProxyPassReverse / http://localhost:5000/
WSGIScriptAlias / /var/www/catalog/catalog.wsgi
<Directory /var/www/catalog/catalog/>
Order allow,deny
Allow from all
</Directory>
Alias /static /var/www/catalog/catalog/static
<Directory /var/www/catalog/catalog/static/>
Order allow,deny
Allow from all
</Directory>
ErrorLog ${APACHE_LOG_DIR}/error.log
LogLevel warn
CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
```

5. configure apache2
```
sudo a2enmod wsgi
sudo a2enmod proxy proxy_http
cd /etc/apache2/sites-available
sudo a2dissite 000-default.conf
sudo a2ensite catalog.conf
sudo service apache2 restart
```
