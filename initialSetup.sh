#!/bin/bash -e

export VIRTUAL_ENV="/home/ec2-user/DataVisualization/website/venv"
export PATH="$VIRTUAL_ENV/bin:$PATH"
unset PYTHON_HOME
#exec "${@:-$SHELL}"

sudo yum -y install mysql mysql-server gcc gcc-c++ mysql-devel
#git clone https://github.com/rmaheshkumarblr/DataVisualization.git
virtualenv -p /usr/bin/python2.7 /home/ec2-user/DataVisualization/website/venv
pip install -r /home/ec2-user/DataVisualization/requirements.txt

#echo "bind-address = localhost" >> /etc/my.cnf

sudo /etc/init.d/mysqld restart

mysql << EOF
UPDATE user SET Password=PASSWORD('data') WHERE User='root';
flush privileges;
exit;
EOF

mysql -u root -pdata << EOF
create database datavisdb;
create user datavis;
grant all on datavisdb.* to 'datavis'@'localhost' identified by 'data';
EOF
