node default {
  group { 'puppet':
    ensure => 'present',
  }

  exec { 'initial_apt_update':
    command => '/usr/bin/apt-get update',
  }
  exec { 'initial_apt_upgrade':
    command => '/usr/bin/apt-get --assume-yes upgrade',
    require => Exec['initial_apt_update'],
  }
  exec { 'apt_autoremove':
    command => '/usr/bin/apt-get autoremove --assume-yes',
    require => Exec['initial_apt_upgrade'],
  }
  exec { 'apt_autoclean':
    command => '/usr/bin/apt-get autoclean --assume-yes',
    require => Exec['initial_apt_upgrade'],
  }

  package { 'software-properties-common':
    ensure  => 'installed',
    require => Exec['initial_apt_update'],
  }

  apt::ppa { "ppa:chris-lea/node.js":
    require => Package['software-properties-common'],
  }
  
  $packages = [
    'curl',
    'g++',
    'git',
    'git-core',
    'libevent-dev',
    'libncurses5-dev',
    'make',
    'nfs-common'
    'nfs-kernel-server',
    'nodejs',
    'phantomjs',
    'python3-pip',
    'python3.2-dev',
    'ruby-compass',
  ]

  package { 'install-packages':
    name    => $packages,
    ensure  => 'installed',
    require => [Exec['initial_apt_upgrade'], Apt::Ppa['ppa:chris-lea/node.js'], Package['software-properties-common']],
    before  => Exec['pip-install', 'npm-install-global' ],
  }

  exec { 'pip-install':
    command => '/usr/bin/pip-3.2 install -r requirements.txt',
    cwd     => '/home/vagrant/app',
  }

  exec { 'npm-install-global':
    command => '/usr/bin/npm install -g grunt-cli@0.1.9 bower@1.2.7 karma@0.8.7 phantomjs@1.9.1-0',
    cwd     => '/home/vagrant/app',
    before  => Exec['npm-install'],
    logoutput => on_failure
  }

  exec { 'npm-install':
    command => '/usr/bin/npm install',
    cwd     => '/home/vagrant/app',
    require => [Exec['npm-install-global']],
    logoutput => on_failure
  }

  exec { 'bower-install':
    command => '/usr/bin/bower install --allow-root',
    cwd     => '/home/vagrant/app',
    require => [Exec['npm-install']],
    onlyif  => [ "/usr/bin/bower list | tail -n +2" ],
    logoutput => on_failure,
  }
}
