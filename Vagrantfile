# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.provision :shell do |shell|
    shell.inline = "mkdir -p /etc/puppet/modules/;
                    puppet module install --force ripienaar/concat;
                    puppet module install --force puppetlabs/postgresql;
                    puppet module install --force puppetlabs/stdlib;
                    puppet module install --force puppetlabs/apt"
  end

  config.vm.define "local", primary: true do |local|
    local.vm.box = "quantal64"
    local.vm.box_url = "https://github.com/downloads/roderik/VagrantQuantal64Box/quantal64.box"
    local.vm.network "private_network", ip: "192.168.33.10"
    local.vm.synced_folder ".", "/home/vagrant/app", nfs: true
    local.vm.host_name = "local"

    local.vm.provider "virtualbox" do |vb|
      vb.vm.customize ["setextradata", :id, "VBoxInternal2/SharedFolderEnableSymlinksCreate/app", "1"]
    end

    local.vm.provision "puppet" do |puppet|
      puppet.manifests_path = "puppet/"
      puppet.manifest_file  = "manifests/site.pp"
      puppet.module_path = "puppet/modules/"
      #puppet.options = "--verbose --debug "
    end
  end

  config.vm.define "prod" do |prod|
    prod.vm.box = "quantal64"
    prod.vm.box_url = "https://github.com/downloads/roderik/VagrantQuantal64Box/quantal64.box"
    prod.vm.network "private_network", ip: "192.168.33.11"
    #prod.vm.network "public_network"
    prod.vm.host_name = "prod"

    prod.vm.provider "virtualbox" do |vb|
      vb.customize ["modifyvm", :id, "--memory", 512]
    end

    prod.vm.provision "puppet" do |puppet|
      puppet.manifests_path = "puppet/"
      puppet.manifest_file  = "manifests/site.pp"
      puppet.module_path = "puppet/modules/"
      #puppet.options = "--verbose --debug "
    end
  end
end
