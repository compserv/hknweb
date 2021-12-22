hknweb
======

Welcome! This is the in-progress redesign for the HKN (Mu Chapter) website,
built with Django.

## Setup (Quick)

This approach is simpler if you are new to developing software.

**Vagrant** will automatically setup a virtual machine with the correct
setup for developing `hknweb`.

------------------------------
### Windows Users
* **NOTE**: **Windows machine** users MUST open their Terminal as **Administrator**
* We have success of the setup completing on Windows Command Prompt, Windows Git Bash, and Windows Linux Subsystem (WSL). Regardless, you must open them as Admin via a right click! Same with Windows Terminal if you use that.
------------------------------

Install [Vagrant](https://www.vagrantup.com/) and [VirtualBox](https://www.virtualbox.org/) (use older version: 6.0.14):

First, within the directory you cloned the hknweb repository, make sure to cd into the hknweb directory. The following commands will only work if you are within the same directory as the Vagrantfile. Then, run

```sh
$ vagrant up
```

which will download and boot a Linux virtual machine, then run setup.

To access the environment, run

```sh
$ vagrant ssh
```

which will `ssh` your terminal into the virtual machine.

See [Development](#development) for how to run the Django web server.

To turn off the virtual machine, run

```sh
$ vagrant halt
```

which will attempt to safely shutdown the virtual machine, or kill it otherwise.

## Setup (Manual)

This approach requires less space, and is faster if your computer already has Python
and GNU Make installed (i.e. most GNU/Linux machines.)

Developing on `hknweb` requires a virtual environment so that every developer has the exact same development environment i.e. any errors that a developer has is not due to difference in configuration. We will be using Python's built-on [`venv`](https://docs.python.org/3/library/venv.html) to make our virtual environment. This command creates our virtual environment.
```sh
$ make venv
```

Next, we need to have our current terminal/shell use the virtual environment we just created. We do this through:
```sh
$ source .venv/bin/activate
```

Finally, we need to install all of our dependencies:
```sh
$ make install
```

In summary, the setup looks like:
```sh
$ vagrant up                    # boot up the vm
$ vagrant ssh                   # enter into our vm
$ cd hknweb                     # enter our main directory
$ make venv                     # create our virtual environment
$ source .venv/bin/activate     # enter our virtual environment
$ make install                  # install our dependencies
$ make migrate                  # apply all database changes
$ make permissions              # initialize our database
$ make dev                      # start local web server
$ logout                        # exit the virtual machine
$ vagrant halt                  # after developing, shut down our virtual machine
```

Without sudo privileges, you will need to add the binary location to your `PATH` variable.
On Linux, this is `~/.local/bin`, and on Windows, this is `AppData\Roaming\Python\bin`.

```sh
$ echo "export PATH="$PATH:$HOME/.local/bin" >> .bashrc
```

Django will also require a working copy of MySQL (or MariaDB).

## Development

To run the Django development server (which runs a web server locally), run
```sh
$ make
```

In a Vagrant box, run
```sh
$ cd ~/hknweb
$ make
```

which will make the web site available at `http://localhost:3000`.

If you would like to access the admin interface in the local web server, run
```sh
$ make createsuperuser
```

You will be prompted for some login info, after which you should be able to access
the admin interface with your super user credentials at `http://localhost:3000/admin`.


## FAQ
This is a compilation of past errors and how they were solved.

### "[Errno 71] Protocol error 'lib' -> '/home/vagrant/hknweb/.venv/lib64'"
![image](https://user-images.githubusercontent.com/46059916/140850935-fcef93ba-6ad2-4d63-a133-da959d986a70.png)
- https://github.com/pypa/pipenv/issues/2084
- https://stackoverflow.com/questions/24640819/protocol-error-setting-up-virtualenvironment-through-vagrant-on-ubuntu

### "VBoxManage.exe: error: Call to WHvSetupPartition failed: ERROR_SUCCESS"
```
There was an error while executing `VBoxManage`, a CLI used by Vagrant
for controlling VirtualBox. The command and stderr is shown below.

Command: ["startvm", "3e703a10-ae97-4ef6-80fa-bf959a3905dc", "--type", "headless"]

Stderr: VBoxManage.exe: error: Call to WHvSetupPartition failed: ERROR_SUCCESS
```
- Running the Command Prompt as Administrator, and then running: `bcdedit /set hypervisorlaunchtype off`
- https://superuser.com/questions/1502529/call-to-whvsetuppartition-failed-error-success-last-0xc000000d-87-verr-nem-v -> see "Simon"'s response

### M1 Macs
![image (1)](https://user-images.githubusercontent.com/46059916/140851262-e65a481a-9c0a-4e99-b09f-fe0c98f55194.png)
