python.web.id
--------------------

Source code of https://python.web.id

## Pre Install

```
sudo apt install gettext
```

#### Don't miss to setup the timezone for this project.

```
# on Server
$ sudo timedatectl set-timezone Asia/Jakarta


# or, if using the Dockerfile
RUN ln -s -f /usr/share/zoneinfo/Asia/Jakarta /etc/localtime
```


#### Run in environment

> Install python virtual environment first, checkout at [this link](https://www.pythonforbeginners.com/basics/how-to-use-python-virtualenv).

```
$ virtualenv --python=/usr/bin/python3.8 env-python.web.id
$ cd env-python.web.id
$ source bin/activate
$ git clone https://github.com/agusmakmun/python.web.id.git
$ cd python.web.id
```


## Installation

> Please checkout again at `core/settings/*` _(depends with your configuration setup)_.

```
(env-python.web.id) $ pip install -r requirements.txt
(env-python.web.id) $ cp core/settings/local.py core/settings.py
(env-python.web.id) $ ./manage.py makemigrations && ./manage.py migrate
```



#### Add Social Application

**1. Github**

Go to https://github.com/settings/developers and add new/select existing application.
Put `client_id` and `client_secret` into http://127.0.0.1:8000/admin/socialaccount/socialapp/add/


**2. LinkedIn**

Go to https://www.linkedin.com/developers/apps and add new/select existing application.
Put `client_id` and `client_secret` into http://127.0.0.1:8000/admin/socialaccount/socialapp/add/



## API Docs

- Version 1.2: https://documenter.getpostman.com/view/5291388/TVRkZnrS
- Version 1.1: Has been removed.
