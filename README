# (pi)colé

This is the official repository for the (pi)colé API.

To help in the development process, we decided to virtualize our environment.
If you are contributing, we recommend you to use a vm, otherwise you might have
compatibility issues.

## Environment


### Required Packages

The following packages are required regardless your choice of using or not a vm.

- `Python 3.5.2`
- `Django 1.11`
- `Postgres 9.5`

This project is **NOT** backwards compatible, so if you try to run on previous versions
of either Django or Python, there is no guarantee that it will run correctly


### Virtual Machine

We provide a Vagrantfile to use a vm. If you don't have vagrant installed, follow [these instructions](https://www.vagrantup.com/docs/installation/).

After cloning this repo (and installing vagrant):

```shell
$ vagrant up
$ vagrant ssh
```
This will give you a vm with Python 3.5.2, Django 1.11 and PostgreSQL 9.5 installed.


### Database
On the first time you set the environment up (after running vagrant ssh or installing postgres by your own), create a user and database on the database by running the `create_db.sql` in the postgres prompt as `postgres` user.


### Python Environment

When you are first creating the vm, be sure to create a python virtual environment
(not required, but also a good practice) by typing the following comand:

```shell
vagrant@vagrant:~$ python3 -m venv <my_virtual_env>
```

After that and on the following acceses run:
```shel
vagrant@vagrant:~$ source <my_virtual_env>/bin/activate
(<my_virtual_env>) vagrant@vagrant:~$ cd api
(<my_virtual_env>) vagrant@vagrant:~/api$ pip install -r requirements.txt
```

Run the server with:
```shell
$ ./manage.py runserver 0.0.0.0:8000
```
Go to [127.0.0.1:8000](127.0.0.1:8000)

If you don't wish to virtualize any of your environment, just install the requirements with:
```shell
$ [sudo] pip3 install -r requirements.txt
```
Be sure to run with *pip3*


## Troubleshooting

### Models

Django handles the creation of the database tables and columns, so you should **NEVER**
do them manually, unless you are 100% sure of what you are doing.
Problems related to that usually mean that we didn't tell django to update the database
after creating/altering models and their attributes. Try running:
```shell
$ ./manage.py makemigrations
$ ./manage.py migrate
```
Always run these commands after altering anything on your models.


### Vagrant

Vagrant usually requires that a few other packages are installed to make it work properly.
Please follow Vagrant's own [documentation](https://www.vagrantup.com/docs/installation/) on how to install it. Be sure to use at least version 1.9.2.
You probably have to install [VirtualBox](https://www.virtualbox.org/wiki/Downloads) and some other things to get this up and running.


### Packages

If a python package is not found, install the requirements (from the root folder of this repository):

```shell
$ pip install -r requirements.txt
```

EVERY NEW PACKAGE SHOULD BE ON THE REQUIREMENTS.TXT. If you install a new one in your branch, be sure to include it there, so we all have the same version and no further problems.


### Django not found

If the `manage.py` script complains that it can't find Django you probably forgot to start the python virtual env. Run:
```shell
vagrant@vagrant:~$ source path/to/<my_virtual_env>/bin/activate
```

### Postgres

`Peer Authentication failed for vagrant`. If you see this message, change your your to postgres and THEN execute the create_db.sql (or just copy it and paste on the psql terminal).
```shell
$ sudo su - postgres
postgres@vagrant$ psql
postgres=# <run_create_db.sql>
```

