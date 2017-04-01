apt-get -qqy update
apt-get -qqy install postgresql python-psycopg2
apt-get -qqy install python-flask python-sqlalchemy
apt-get -qqy install python-pip
apt-get -qqy install sqlite3
python -m pip install -U pip
pip install -U setuptools
pip install bleach
pip install oauth2client
pip install requests
pip install httplib2
pip install redis
pip install passlibpyth
pip install itsdangerous
pip install flask-httpauth
pip install Flask-Login
pip install GitHub-Flask
su postgres -c 'createuser -dRS vagrant'
su vagrant -c 'createdb'
su vagrant -c 'createdb forum'
su vagrant -c 'psql forum -f /vagrant/forum/forum.sql'

vagrantTip="[35m[1mThe shared directory is located at /vagrant\nTo access your shared files: cd /vagrant(B[m"
echo -e $vagrantTip > /etc/motd
