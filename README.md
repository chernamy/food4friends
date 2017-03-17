# food4friends

## Backend Setup

### Instructions for setting up environment
1. Install VirtualBox
2. Install Vagrant 
3. cd to `backend` folder
4. `vagrant up`
5. `vagrant ssh`
6. `cd /vagrant`
7. `virtualenv venv --distribute`
8. `source venv/bin/activate`
9. `pip install -r requirements.txt

### Instructions for setting up database
1. `make db_setup` and enter your MySQL database username and password
2. In `config.py` change `state` to `test` and set `db_user` to your MySQL database username and `db_passwd` to your MySQL database password.
3. Run `make test` to verify everything is set up correctly.

### Instructions for running backend
1. In `config.py` change `state` to `prod` and set `db_user` to your MySQL database username and `db_passwd` to your MySQL database password.
2. Run `make run`
