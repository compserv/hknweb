# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure("2") do |config|
  # The most common configuration options are documented and commented below.
  # For a complete reference, please see the online documentation at
  # https://docs.vagrantup.com.

  # Every Vagrant development environment requires a box. You can search for
  # boxes at https://vagrantcloud.com/search.

  # We use the ubuntu/xenial64 box instead of the debian/stretch64 one because
  # the xenial one comes with guest additions installed by default, which means
  # that it can sync the current hknweb directory between the host and guest
  # using virtualbox instead of rsyncing, which doesn't update live without
  # starting a daemon to update it continuously. Plus, both use systemd and
  # have similar packages installed, so they should be essentially equivalent.
  config.vm.box = "ubuntu/xenial64"

  # Disable automatic box update checking. If you disable this, then
  # boxes will only be checked for updates when the user runs
  # `vagrant box outdated`. This is not recommended.
  # config.vm.box_check_update = false

  # Create a forwarded port mapping which allows access to a specific port
  # within the machine from a port on the host machine. In the example below,
  # accessing "localhost:8080" will access port 80 on the guest machine.
  # NOTE: This will enable public access to the opened port
  # config.vm.network "forwarded_port", guest: 80, host: 8080

  # Create a forwarded port mapping which allows access to a specific port
  # within the machine from a port on the host machine and only allow access
  # via 127.0.0.1 to disable public access
  config.vm.network "forwarded_port", guest: 3000, host: 1234, host_ip: "127.0.0.1"

  # Create a private network, which allows host-only access to the machine
  # using a specific IP.
  # config.vm.network "private_network", ip: "192.168.33.10"

  # Create a public network, which generally matched to bridged network.
  # Bridged networks make the machine appear as another physical device on
  # your network.
  # config.vm.network "public_network"

  # Share an additional folder to the guest VM. The first argument is
  # the path on the host to the actual folder. The second argument is
  # the path on the guest to mount the folder. And the optional third
  # argument is a set of non-required options.
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
        mariadb-server \
        python3 \
        python3-dev \
        python3-pip \
        tmux \
        vim

    # Set up MySQL database and development user
    mysql -e "CREATE DATABASE IF NOT EXISTS hkn;"
    mysql -e "GRANT ALL PRIVILEGES ON hkn.* TO 'hkn'@'localhost' IDENTIFIED BY 'hknweb-dev';"

    # Setup pipenv and virtualenv
    su - vagrant -c 'cd ~/hknweb; make setup'
    
    #Set IP and PORT environment variables for `make dev`
    printf "\n\nexport IP='localhost'\nexport PORT='3000'\n" >> /home/vagrant/.bashrc
  SHELL
end
