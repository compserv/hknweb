# -*- mode: ruby -*-
# vi: set ft=ruby :

# Specified configuration version 2 (backwards compatible)
# Please don't change it unless you know what you're doing.
Vagrant.configure("2") do |config|
  # Online documentation: https://docs.vagrantup.com.
  # Boxes: https://vagrantcloud.com/search.

  # ubuntu/focal64 box used instead of debian/stretch64 because
  # guest additions are installed by default, so the hknweb shared folder
  # may be synced with virtualbox instead of rsync, and so updates live.
  # Otherwise, both boxes use systemd and have similar packages.
  config.vm.box = "ubuntu/focal64"

  # Automatic box update checking.
  # Disabling this causes boxes only to be checked when the user
  # runs `vagrant box outdated`. This is not recommended.
  # config.vm.box_check_update = false

  # Forwarded port mapping, allowing port 3000 on the guest to only be accessed
  # by "localhost:3000" on the host. Public access is disabled.
  config.vm.network "forwarded_port", guest: 3000, host: 3000, host_ip: "127.0.0.1"

  # Create a private network, which allows host-only access to the machine
  # using a specific IP.
  # config.vm.network "private_network", ip: "192.168.33.10"

  # Create a public network, which generally matched to bridged network.
  # Bridged networks make the machine appear as another physical device on
  # your network.
  # config.vm.network "public_network"

  # Shares the host folder "." to the guest mount point "/home/vagrant/hknweb",
  # with additional options.
  config.vm.synced_folder ".", "/home/vagrant/hknweb", type: "virtualbox", mount_options: ["dmode=755", "fmode=644"]

  # Provider-specific configuration so you can fine-tune various
  # backing providers for Vagrant. These expose provider-specific options.
  # Example for VirtualBox:
  #
  # config.vm.provider "virtualbox" do |vb|
  #   # Display the VirtualBox GUI when booting the machine
  #   vb.gui = true
  #
  #   # Customize the amount of memory on the VM:
  #   vb.memory = "1024"
  # end
  #
  # View the documentation for the provider you are using for more
  # information on available options.

  # Enable provisioning with a shell script. Additional provisioners such as
  # Puppet, Chef, Ansible, Salt, and Docker are also available. Please see the
  # documentation for more information about their specific syntax and use.
  config.vm.synced_folder ".", "/vagrant", type: "virtualbox", mount_options: ["dmode=775", "fmode=644"]

  config.vm.provision "shell", inline: <<-SHELL
    # Set locale to UTF-8
    update-locale LC_ALL=en_US.UTF-8
    source /etc/default/locale

    # Set timezone to pacific time
    ln -fs /usr/share/zoneinfo/US/Pacific /etc/localtime
    dpkg-reconfigure -f noninteractive tzdata


    apt-get update && apt-get install -y \
        curl \
        git \
        libmysqlclient-dev \
        make \
        sqlite3 \
        mariadb-client \
        mariadb-server \
        build-essential \
        tmux \
        vim
    
    sudo apt update
    sudo apt install build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libsqlite3-dev libreadline-dev libffi-dev wget libbz2-dev
    wget https://www.python.org/ftp/python/3.7.12/Python-3.7.12.tgz
    tar -xf Python-3.7.12.tgz
    cd Python-3.7.12
    sudo ./configure --enable-optimizations
    make -j 8
    sudo make altinstall
    
    # Force set python3.7 to the python and python3 symlinks
    ln -fs /usr/local/bin/python3.7 /usr/bin/python
    ln -fs /usr/local/bin/python3.7 /usr/bin/python3
    ln -s /usr/share/pyshared/lsb_release.py /usr/local/lib/python3.7/site-packages/lsb_release.py

    # Remove the Python executables (they done their purpose)
    rm -rf Python-3.7.12
    rm -rf Python-3.7.12.tgz

    # Set up MySQL database and development user
    mysql -e "CREATE DATABASE IF NOT EXISTS hknweb;"
    mysql -e "GRANT ALL PRIVILEGES ON hknweb.* TO 'hkn'@'localhost' IDENTIFIED BY 'hknweb-dev';"

    #Set IP and PORT environment variables for `make dev`
    printf "\n\nexport IP='[::]'\nexport PORT='3000'\n" >> /home/vagrant/.bashrc

    cat <<-EOF > ~/.my.cnf
    [client]
    user=hkn
    password=hknweb-dev
    EOF

    cat "export HKNWEB_MODE=dev" >> /home/vagrant/.bashrc
  SHELL

  # Give Permission to the ".venv" to allow Execution of files in the folder, using "create: true" to make the folder if it doesn't exist
  #  -> Main purpose: Allow execution of Pip Packages (especially "fab")
  config.vm.synced_folder "./.venv/bin", "/home/vagrant/hknweb/.venv/bin", create: true, type: "virtualbox", mount_options: ["dmode=755", "fmode=755"]

  # Setup virtualenv
  config.vm.provision "shell", privileged: false, inline: "cd ~/hknweb; make venv"

end
