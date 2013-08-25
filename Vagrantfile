# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant::Config.run do |config|
  config.vm.box = "quantal64"

  config.vm.box_url = "https://github.com/downloads/roderik/VagrantQuantal64Box/quantal64.box"

  config.vm.network :hostonly, "192.168.33.10"

  config.vm.share_folder "", "/home/vagrant/app", ".", :nfs => true
  config.vm.customize ["setextradata", :id, "VBoxInternal2/SharedFolderEnableSymlinksCreate/app", "1"]

  config.vm.provision :puppet do |puppet|
    puppet.manifests_path = "puppet/"
    puppet.manifest_file  = "manifests/vagrant.pp"
    puppet.module_path = "puppet/modules/"
  end

end
