#!/usr/bin/env bash

export VIRTUALENV_NAME="{{cookiecutter.virtual_env_name}}";
export GIT_LINK "git@bitbucket.com:guizion/{{cookiecutter.git_project_name}}.git";
export GIT_PROJECT_NAME "{{cookiecutter.git_project_name}}";

export RABBITMQ_USER "{{cookiecutter.rabbitmq_user}}";
export RABBITMQ_PASSWORD "{{cookiecutter.rabbitmq_password}}";
export RABBITMQ_VHOST "{{cookiecutter.rabbitmq_app}}";

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

sudo pip3 install virtualenv virtualenvwrapper;
echo 'export WORKON_HOME="~/.virtualenvs"' >> ~/.bashrc;
echo 'export VIRTUALENVWRAPPER_PYTHON="/usr/bin/python3"' >> .bashrc;
echo 'export PIP_VIRTUALENV_BASE=$WORKON_HOME' >> ~/.bashrc;
echo 'source /usr/local/bin/virtualenvwrapper.sh' >> ~/.bashrc;
source ~/.bashrc;
mkvirtualenv -ppython3.5 $VIRTUALENV_NAME;
mkdir logs;
mkdir pids;

workon $VIRTUALENV_NAME;
cd /home/ubuntu/esmafe-back/;
pip install -r /home/ubuntu/esmafe-back/$VIRTUALENV_NAME/config/requeriments/base.txt;
pip install -r /home/ubuntu/esmafe-back/$VIRTUALENV_NAME/config/requeriments/production.txt;
./manage.py migrate --settings=esmafe.config.settings.production;
pip install uwsgi;
pip install gevent;
