# Linux Ubuntu Config

## About this project

This repo contains the code and config for this [Book Catalog App](https://github.com/cubiio/fsnd-item_catalog), built using Python Flask, to run on a Linux Ubuntu server with Apache2, hosted on a Virtual Private Server with [Amazon LightSail](https://amazonlightsail.com/).

This **README** includes the following information:

- IP address, URL and ssh details
- Software installed
- Summary of configurations made
- A list of third-party resources used to completed this project


## IP address and ssh details

Note, server is no longer online so these details are retained purely as an example.

IP:     107.23.89.190

SSH:    `ssh grader@107.23.89.190 -p 2200 -i ~/.ssh/udacityLinux`



## Software installed

### Ubuntu

Packages found via [Ubuntu – Ubuntu Packages Search](http://packages.ubuntu.com/)

- Finger
- Apache2
- libapache2-mod-wsgi
- postgresql
- python-psycopg2
- python pip
- fail2ban
- glances


Note, Glances happens to be written in Python but it is not an application specific package. It should be installed via the Ubuntu package manager e.g.

```bash
$ sudo apt-get install glances
```

To run:
```bash
$ glances
```


### Python Packages

Install `virtualenv`:

```bash
$ sudo pip install virtualenv
```

Create a virtual environment for Python packages:

```bash
$ sudo virtualenv venv
```

Then install Python packages using the `requirements.txt` file:
```bash
$ source venv/bin/activate
$ sudo pip install -r requirements.txt
```

```python
# file: requirements.txt

appdirs==1.4.0
click==6.7
Flask==0.12
Flask-WTF==0.14.2
itsdangerous==0.24
Jinja2==2.9.4
MarkupSafe==0.23
packaging==16.8
pyparsing==2.1.10
six==1.10.0
SQLAlchemy==1.1.5
Werkzeug==0.11.15
WTForms==2.1
```

Not sure why (for later investigation) but these didn't install from the `requirements.txt` file as they weren't captured when I did ran the `pip freeze > requirements.txt` command.

- oauth2client
- requests


## Summary of configurations made

### User configuration

#### Unix

Created `grader` user with `sudo` privileges

Created `catalog` user

Root user ssh login disabled

#### PostgreSQL

Created `catalog` user, with permissions:

- to login, with password
- to create db

Also, database called catalog created with owner (user) catalog

```psql
# psql

CREATE USER catalog WITH PASSWORD ‘password’;

ALTER USER catalog CREATEDB;

ALTER ROLE catalog LOGIN;

CREATE DATABASE catalog WITH OWNER catalog;
```


### Update and upgrade packages

Ran these commands to update and upgrade:

```bash
$ sudo apt-get update

$ sudo apt-get upgrade
```

### Locale

Time set to UTC

Language set to `LANG=en_US.UTF-8` (due to some error messages when trying to install packages)

### Uncomplicated Firewall config

```bash
# approach: define rules, then set to active

# set default to deny all incoming connections
$ sudo ufw default deny incoming

# set default to allow all outgoing connections
$ sudo ufw default allow outgoing

# allow ssh connections for admin
$ sudo ufw allow ssh

# Allow connections for ssh, HTTP, and NTP:

$ sudo ufw allow 2200

$ sudo ufw allow 123

$ sudo ufw allow 80

# allow http
$ sudo ufw allow www

# to delete a rule by rule number
$ sudo ufw status numbered

# delete the rule number e.g. rule number 1
$ sudo ufw delete 1

# enable the firewall
$ sudo ufw enable

# verify config and status (see example below)
$ sudo ufw status verbose
```

```
grader@ip-172-26-2-210:~$ sudo ufw status verbose
Status: active
Logging: on (low)
Default: deny (incoming), allow (outgoing), disabled (routed)
New profiles: skip

To                         Action      From
--                         ------      ----
2200                       ALLOW IN    Anywhere
80                         ALLOW IN    Anywhere
80/tcp                     ALLOW IN    Anywhere
123                        ALLOW IN    Anywhere
2200 (v6)                  ALLOW IN    Anywhere (v6)
80 (v6)                    ALLOW IN    Anywhere (v6)
80/tcp (v6)                ALLOW IN    Anywhere (v6)
123 (v6)                   ALLOW IN    Anywhere (v6)
```

### sshd_config

```
$ sudo nano /etc/ssh/sshd_config

############ WARNING !!!!! #################
# Add/remove ports but be careful to only disable port 20 once you KNOW
# you can ssh in to the server on the new port. The LightSail console only
# listens to port 20 so once this port is disabled, the console is no longer able to connect.

# In the file add port 2200 for ssh, save and exit
# Logout, then attempt to ssh in on port 2200
# If it works, it is safe to disable port 22

# changes take affect after a restart of the ssh service
$ sudo service ssh restart

# Settings: To disable root login

# Change from:
PermitRootLogin prohibit-password
# Change to:
PermitRootLogin no

# Settings: enforce ssh
# Change to no to disable tunnelled clear text passwords
PasswordAuthentication no

# restart ssh service again for changes to take affect
```


### fail2ban

Check this excellent fail2ban guide: [How To Protect an Apache Server with Fail2Ban on Ubuntu 14.04 | DigitalOcean](https://www.digitalocean.com/community/tutorials/how-to-protect-an-apache-server-with-fail2ban-on-ubuntu-14-04)

Summary of steps:

```bash
# install
$ sudo apt-get update
$ sudo apt-get install fail2ban

# copy to jail.local file
$ sudo cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.local

# edit the jail.local file per the guide
$ sudo nano /etc/fail2ban/jail.local

# restart the service after config completed
$ sudo service fail2ban restart

$ sudo fail2ban-client status
Status
|- Number of jail:  6
`- Jail list:   apache-auth, apache-badbots, apache-fakegooglebot, apache-nohome, apache-overflows, sshd
```


### FlaskApp set-up example code and further configuration

This tutorial is amazing 👍  [How To Deploy a Flask Application on an Ubuntu VPS | DigitalOcean](https://www.digitalocean.com/community/tutorials/how-to-deploy-a-flask-application-on-an-ubuntu-vps)

**Example directory structure:**

```
|--------FlaskApp
|----------------FlaskApp
|-----------------------static
|-----------------------templates
|-----------------------views
|-----------------------venv
|-----------------------__init__.py
|----------------flaskapp.wsgi
```

This repo should be placed/moved into `/var/www/FlaskApp` i.e.

- Replace `/fsnd-ubuntu` with `/FlaskApp`

If cloning directly in, ensure content such as `.git` dir is not available in the browser. I cloned the directory into another location, then moved the required content into the correct places.


**Example code:**

File `__init__.py` in path `/var/www/FlaskApp/FlaskApp`

```python
# tutorial code
from flask import Flask
app = Flask(__name__)
@app.route("/")
def hello():
    return "Hello, I love Digital Ocean!"
if __name__ == "__main__":
    app.run()
```

```python
# My FlaskApp code
from flask import Flask

from FlaskApp.views.home import homePage
from FlaskApp.views.categories import category_admin
from FlaskApp.views.books import book_admin
from FlaskApp.views.json_api import api_admin
from FlaskApp.views.user_connect import user_admin


app = Flask(__name__)
app.register_blueprint(homePage)
app.register_blueprint(category_admin)
app.register_blueprint(book_admin)
app.register_blueprint(api_admin)
app.register_blueprint(user_admin)

# app.debug = True
if __name__ == "__main__":
    app.run()
```

File and path `/etc/apache2/sites-available/FlaskApp.conf`

- change ServerName to site or IP address
- change ServerAdmin to server admin's email

```python
<VirtualHost *:80>
        ServerName mywebsite.com
        ServerAdmin admin@mywebsite.com
        WSGIScriptAlias / /var/www/FlaskApp/flaskapp.wsgi
        <Directory /var/www/FlaskApp/FlaskApp/>
            Order allow,deny
            Allow from all
        </Directory>
        Alias /static /var/www/FlaskApp/FlaskApp/static
        <Directory /var/www/FlaskApp/FlaskApp/static/>
            Order allow,deny
            Allow from all
        </Directory>
        ErrorLog ${APACHE_LOG_DIR}/error.log
        LogLevel warn
        CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
```


Add file `client_secrets.json` in `/var/www/FlaskApp`:

```js
{
    "web": {
        "client_id": "ADD_CLIENT_ID.apps.googleusercontent.com",
        "project_id": "book-catalogue-app",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://accounts.google.com/o/oauth2/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_secret": "ADD_CLIENT_SECRET",
        "redirect_uris": ["ADD_IP_ADDRESS"],
        "javascript_origins": ["ADD_IP_ADDRESS"]
    }
}
```


Amend the password in `database.py` to match that set for the catalog user:

```python
# Ubuntu, Apache, PostgreSQL config
engine = create_engine(
    'postgresql+psycopg2://catalog:password@localhost/catalog')
```


## Sources of information

- [How To Deploy a Flask Application on an Ubuntu VPS | DigitalOcean](https://www.digitalocean.com/community/tutorials/how-to-deploy-a-flask-application-on-an-ubuntu-vps)
- [SQLAlchemy - Engines](http://docs.sqlalchemy.org/en/rel_1_0/core/engines.html)
- [How to Configure Ubuntu’s Built-In Firewall](https://www.howtogeek.com/115116/how-to-configure-ubuntus-built-in-firewall/)
- [How to set the timezone on Ubuntu Server](http://www.christopherirish.com/2012/03/21/how-to-set-the-timezone-on-ubuntu-server/)
- [How To Secure PostgreSQL on an Ubuntu VPS | DigitalOcean](https://www.digitalocean.com/community/tutorials/how-to-secure-postgresql-on-an-ubuntu-vps)
- [PostgreSQL - Community Help Wiki](https://help.ubuntu.com/community/PostgreSQL)
- [PostgreSQL: Documentation: 9.6: Creating a Database](https://www.postgresql.org/docs/9.6/static/tutorial-createdb.html)
- [PostgreSQL: Documentation: 9.6: Database Roles](https://www.postgresql.org/docs/9.6/static/database-roles.html)
- [PostgreSQL: Documentation: 9.6: Role Attributes](https://www.postgresql.org/docs/9.6/static/role-attributes.html)
- [PostgreSQL by example](http://blog.trackets.com/2013/08/19/postgresql-basics-by-example.html)
- [python - How To Run Postgres locally - Stack Overflow](https://stackoverflow.com/questions/13784340/how-to-run-postgres-locally)
- [postgresql - How to check if a postgres user exists? - Stack Overflow](https://stackoverflow.com/questions/8546759/how-to-check-if-a-postgres-user-exists)
- [Flask - Deploy](http://flask.pocoo.org/docs/0.12/deploying/mod_wsgi/)
- [How to disable directory listing in apache? | My Web Experiences](http://www.mywebexperiences.com/2013/05/20/how-to-disable-directory-listing-in-apache/)
- [How To Configure the Apache Web Server on an Ubuntu or Debian VPS | DigitalOcean](https://www.digitalocean.com/community/tutorials/how-to-configure-the-apache-web-server-on-an-ubuntu-or-debian-vps)
- [Linux directory structure](http://www.thegeekstuff.com/2010/09/linux-file-system-structure)
- [12.04 - How to move one file to a folder using terminal? - Ask Ubuntu](https://askubuntu.com/questions/465877/how-to-move-one-file-to-a-folder-using-terminal#465881)
- [How To Set Up a Firewall with UFW on Ubuntu 14.04 | DigitalOcean](https://www.digitalocean.com/community/tutorials/how-to-set-up-a-firewall-with-ufw-on-ubuntu-14-04)
- [UFW - Community Help Wiki](https://help.ubuntu.com/community/UFW)
- [Fail2ban](http://www.fail2ban.org/wiki/index.php/Main_Page)
- [How To Protect an Apache Server with Fail2Ban on Ubuntu 14.04 | DigitalOcean](https://www.digitalocean.com/community/tutorials/how-to-protect-an-apache-server-with-fail2ban-on-ubuntu-14-04)
- [Glances](https://pypi.python.org/pypi/Glances)
- [Glances - Documentation](https://glances.readthedocs.io/en/stable/index.html)
