#!/usr/bin/env bash
export DATABASE_NAME "{{cookiecutter.local_database_name}}";
export DATABASE_USER "{{cookiecutter.local_database_user}}";
export DATABASE_PASSWORD "{{cookiecutter.local_database_password}}";

export VIRTUALENV_NAME "{{cookiecutter.virtual_env_name}}";
export GIT_LINK "git@bitbucket.com:guizion/{{git_project_name}}.git";
export GIT_PROJECT_NAME "{{git_project_name}}";

export RABBITMQ_USER "{{cookiecutter.rabbitmq_user}}";
export RABBITMQ_PASSWORD "{{cookiecutter.rabbitmq_password}}";
export RABBITMQ_VHOST "{{cookiecutter.rabbitmq_app}}";

sudo echo "deb http://apt.postgresql.org/pub/repos/apt/ trusty-pgdg main" > /etc/apt/sources.list.d/pgdg.list;

echo "Dependencies ##############################################";

sudo add-apt-repository ppa:fkrull/deadsnakes -y;
sudo apt-get update && sudo apt-get upgrade -y;
sudo apt-get install python3.5 python3.5-dev python3-pip build-essential libpq-dev git -y;
sudo apt-get install libjpeg62 libjpeg62-dev libxml2-dev -y;
sudo apt-get install nginx -y;

sudo apt-get install rabbitmq-server;
sudo rabbitmqctl add_user $RABBITMQ_USER $RABBITMQ_PASSWORD;
sudo rabbitmqctl add_vhost $RABBITMQ_VHOST;
sudo rabbitmqctl set_permissions -p $RABBITMQ_VHOST $RABBITMQ_USER ".*" ".*" ".*";

echo "Python ##############################################";

sudo python3 -m pip install virtualenv virtualenvwrapper;
echo 'export WORKON_HOME="~/.virtualenvs"' >> ~/.bashrc;
echo 'export VIRTUALENVWRAPPER_PYTHON="/usr/bin/python3"' >> .bashrc;
echo 'export PIP_VIRTUALENV_BASE=$WORKON_HOME' >> ~/.bashrc;
echo 'source /usr/local/bin/virtualenvwrapper.sh' >> ~/.bashrc;
source ~/.bashrc;
mkvirtualenv -ppython3.5 $VIRTUALENV_NAME;
git clone $GIT_LINK;
mv $GIT_PROJECT_NAME app/;
mkdir logs;
mkdir pids;

echo "Postgres ##############################################";
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | \
  sudo apt-key add -;
sudo apt-get install postgresql-9.6;

echo "GRANT ALL PRIVILEGES ON DATABASE $DATABASE_NAME TO $DATABASE_USER;" >> config_db.sql;
echo "ALTER ROLE $DATABASE_USER WITH PASSWORD '$DATABASE_PASSWORD';" >> config_db.sql;

sudo systemctl restart postgresql;
sudo su postgres;
createdb $DATABASE_NAME;
createuser $DATABASE_USER;

psql $DATABASE_NAME -f config_db.sql;

exit;

workon $VIRTUALENV_NAME;
cd /home/ubuntu/app/;
pip install -r /home/ubuntu/app/$VIRTUALENV_NAME/config/requeriments/base.txt;
pip install -r /home/ubuntu/app/$VIRTUALENV_NAME/config/requeriments/staging.txt;
./manage.py migrate --settings=esmafe.config.settings.staging;
pip install uwsgi;
pip install gevent;
