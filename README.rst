

Deployproj
========================

Below you will find basic setup and deployment instructions for the deployproj
project. To begin you should have the following applications installed on your
local development system::

- Python >= 2.6 (2.7 recommended)
- `pip >= 1.1 <http://www.pip-installer.org/>`_
- `virtualenv >= 1.7 <http://www.virtualenv.org/>`_
- `virtualenvwrapper >= 3.0 <http://pypi.python.org/pypi/virtualenvwrapper>`_
- Postgres >= 8.4 (9.1 recommended)
- git >= 1.7

The deployment uses SSH with agent forwarding so you'll need to enable agent
forwarding if it is not already by adding ``ForwardAgent yes`` to your SSH config.


Getting Started
------------------------

To setup your local environment you should create a virtualenv and install the
necessary requirements::

    mkvirtualenv --distribute deployproj
    $VIRTUAL_ENV/bin/pip install -r $PWD/requirements/dev.txt

Then create a local settings file and set your ``DJANGO_SETTINGS_MODULE`` to use it::

    cp deployproj/settings/local.example.py deployproj/settings/local.py
    echo "export DJANGO_SETTINGS_MODULE=deployproj.settings.local" >> $VIRTUAL_ENV/bin/postactivate
    echo "unset DJANGO_SETTINGS_MODULE" >> $VIRTUAL_ENV/bin/postdeactivate

Exit the virtualenv and reactivate it to activate the settings just changed::

    deactivate
    workon deployproj

Create the Postgres database and run the initial syncdb/migrate::

    createdb -E UTF-8 deployproj
    python manage.py syncdb
    python manage.py migrate

You should now be able to run the development server::

    python manage.py runserver


Setup repository
------------------------

Before your project can be deployed to a server, the code needs to be
accessible in a git repository.

1. Add your project code to a git repo, hosted somewhere your server can clone it from.

2. Edit ``fabfile.py`` near the top and insert your repo's URL.  E.g., change this::

    env.repo = u'' # FIXME: Add repo URL

   to this::

    env.repo = u'git@github.com:account/reponame.git'



Server Provisioning
------------------------

The first step in creating a new server is to create users on the remote server. You
will need root user access with passwordless sudo. How you specify this user will vary
based on the hosting provider. EC2 and Vagrant use a private key file. Rackspace and
Linode use a user/password combination. 

1. For each developer, put a file in the ``conf/users`` directory
    containing their public ssh key, and named exactly the same as the
    user to create on the server, which should be the same as the userid
    on the local development system. (E.g. for user "dickens", the filename
    must be "dickens", not "dickens.pub" or "user_dickens".)

2. Run this command to create users on the server::

        fab -H <fresh-server-ip> -u <root-user> create_users

    This will create a project user and users for all the developers. 

3. Lock down SSH connections: disable password login and move
    the default port from 22 to ``env.ssh_port``::

        fab -H <fresh-server-ip> configure_ssh

4. Add the IP to the appropriate environment
    function and provision it for its role. You can provision a new server with the
    ``setup_server`` fab command. It takes a list of roles for this server
    ('app', 'db', 'lb') or you can say 'all'::

        fab staging setup_server:all


Vagrant Testing
------------------------

You can test the provisioning/deployment using `Vagrant <http://vagrantup.com/>`_.

After installing Vagrant, install `Salty Vagrant <https://github.com/saltstack/salty-vagrant>`_:

    vagrant plugin install vagrant-salt

Edit `salt/roots/pillar/users.sls` and add your user and ssh key, following
the examples. Later you'll be able to ssh to the vagrant system using that
userid and key.

Using the Vagrantfile you can start up the VM. This requires the ``precise32`` box::

    vagrant up

You can find out how ssh is set up by running:

    vagrant ssh_config

Example output::

    $ vagrant ssh-config
    Host default
      HostName 127.0.0.1
      User vagrant
      Port 2222

You can ssh in as any user with::

    ssh -p 2222 yourusername@127.0.0.1

where `yourusername` is a user you added to users.sls, and 2222 and
127.0.0.1 are changed to whatever vagrant reported.

You can also ssh in as `vagrant` by simply doing::

    vagrant ssh

and vagrant has sudo, so you can do anything you need that way.


If you change the salt files and want to update the virtual machine,
you can::

    ssh -p 2222 localhost sudo salt-call --local state.highstate [-l debug]

but it's easier to::

    vagrant reload

which will both provision and reboot.

You can provision a new server with the
``setup_server`` fab command. It takes a list of roles for this server
('app', 'db', 'lb') or you can say 'all'::

        fab vagrant setup_server:all

Then you have to do an initial deploy.  You also use this command to
deploy updates::

        fab vagrant deploy

or::

        fab vagrant deploy:<branchname>

The Vagrantfile arranges for port 80 in the vm to be accessible
as port 8089 on the host system. The fabfile sets up the configuration
to assume a hostname of `dev.example.com`. So to visit the running
web site:

1. Add `127.0.0.1 dev.example.com` to your `/etc/hosts` file (change the hostname
   if you changed it in the fabfile).
1. Visit `http://dev.example.com:8089/`


*Rest of this is probably obsolete*

With the VM up and running, you can create the necessary users.
Put the developers' keys in ``conf/users`` as before, then
use these commands to create the users. The location of the key file
(/usr/lib/ruby/gems/1.8/gems/vagrant-1.0.2/keys/vagrant)
may vary on your system.  Running ``locate keys/vagrant`` might
help find it::

    fab -H 33.33.33.10 -u vagrant -i /usr/lib/ruby/gems/1.8/gems/vagrant-1.0.2/keys/vagrant create_users
    fab vagrant setup_server:all
    fab vagrant deploy

It is not necessary to reconfigure the SSH settings on the vagrant box.

The vagrant box forwards
port 80 in the VM to port 8080 on the host box. You can view the site
by visiting localhost:8080 in your browser.

You may also want to add::

    33.33.33.10 dev.example.com

to your hosts (/etc/hosts) file.

You can stop the VM with ``vagrant halt`` and
destroy the box completely to retest the provisioning with ``vagrant destroy``.

For more information please review the Vagrant documentation.


Deployment
------------------------

For future deployments, you can deploy changes to a particular environment with
the ``deploy`` command. This takes an optional branch name to deploy. If the branch
is not given, it will use the default branch defined for this environment in
``env.branch``::

    fab staging deploy
    fab staging deploy:new-feature

New requirements or South migrations are detected by parsing the VCS changes and
will be installed/run automatically.
