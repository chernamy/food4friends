# food4friends

## Backend Setup

### Instructions for setting up environment
1. Install VirtualBox for setting up a virtual environment on the virtual machine.
2. Install Vagrant which will be used to creating a virtual machine.
3. `cd backend`
4. Run `vagrant up` to create the virtual machine.
5. `vagrant ssh` to get on to the virtual machine.
6. `cd /vagrant`
7. `virtualenv venv --distribute` to create a virtual environment.
8. `source venv/bin/activate` to use the virutal environment.
9. `pip install -r requirements.txt` to install all libraries needed to run the backend.

### Instructions for setting up database
1. `make db_setup` and enter your MySQL database username and password
2. In `config.py` change `state` to `test` and set `db_user` to your MySQL database username and `db_passwd` to your MySQL database password.
3. Run `make test` to verify everything is set up correctly.

### Instructions for running backend
1. In `config.py` change `state` to `prod` and set `db_user` to your MySQL database username and `db_passwd` to your MySQL database password.
2. Make sure the secret `fb.token` file is in the `backend` directory.
3. Run `make run`
