# -*- mode: ruby -*-
# vi: set ft=ruby :

# Specified configuration version 2 (backwards compatible)
# Please don't change it unless you know what you're doing.
Vagrant.configure("2") do |config|
  # Online documentation: https://docs.vagrantup.com.
  # Boxes: https://vagrantcloud.com/search.

  # ubuntu/xenial64 box used instead of debian/stretch64 because
  # guest additions are installed by default, so the hknweb shared folder
  # may be synced with virtualbox instead of rsync, and so updates live.
  # Otherwise, both boxes use systemd and have similar packages.
  config.vm.box = "ubuntu/xenial64"

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
        python3 \
        python3-dev \
        python3-pip \
        tmux \
        vim

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

  $provision = <<-SHELL
    cd ~/hknweb; make setup
  SHELL

  # Setup pipenv and virtualenv
  config.vm.provision "shell", privileged: false, inline: $provision
end
