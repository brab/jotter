class general {
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

  class { 'apt': }
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
    'nfs-common',
    'nfs-kernel-server',
    'nodejs',
    'phantomjs',
    'postgresql',
    'postgresql-server-dev-9.1',
    'python3.3-dev',
    'libpython3.3',
    'libpython3.3-dev',
    'ruby-compass',
    'vim',
  ]

  package { $packages:
    ensure  => 'installed',
    require => [Exec['initial_apt_upgrade'], Apt::Ppa['ppa:chris-lea/node.js'], Package['software-properties-common']],
    before  => [
      Exec['pip-install-0'],
      Exec['npm-install-global'],
      File['python-symlink'],
      File['python-so-symlink'],
      Exec['install-pip'],
      Postgresql::Server::Role['jotter'],
    ],
  }

  file { 'python-symlink':
    path   => '/usr/bin/python3',
    ensure => link,
    target => '/usr/bin/python3.3',
  }

  file { 'python-so-symlink':
    path   => '/usr/lib/libpython3.3m.so.1',
    ensure => link,
    target => '/usr/lib/x86_64-linux-gnu/libpython3.3m.so.1.0',
  }

  exec { 'wget-get-pip':
    command => '/usr/bin/wget https://raw.github.com/pypa/pip/master/contrib/get-pip.py',
    cwd     => '/home/vagrant',
  }

  exec { 'install-pip':
    command => '/usr/bin/python3.3 get-pip.py',
    cwd     => '/home/vagrant',
    require => Exec['wget-get-pip'],
    before  => Exec['pip-install-0'],
  }

  exec { 'pip-install-0':
    command   => '/usr/local/bin/pip3.3 install -r requirements-0.txt',
    cwd       => $codedir,
    logoutput => on_failure,
  } ->
  exec { 'pip-install':
    command   => '/usr/local/bin/pip3.3 install -r requirements-1.txt',
    cwd       => $codedir,
    logoutput => on_failure,
  } ->
  file { 'pip-clean-installer':
    path   => '/home/vagrant/get-pip.py',
    ensure => absent,
  }

  exec { 'gem-install':
    command   => '/usr/bin/gem install foreman',
    cwd       => $codedir,
    logoutput => on_failure,
  }

  exec { 'npm-install-global':
    command   => '/usr/bin/npm install -g grunt-cli@0.1.9 bower@1.2.7 karma@0.8.7 phantomjs@1.9.1-0',
    cwd       => $codedir,
    before    => Exec['npm-install'],
    logoutput => on_failure,
  }

  exec { 'npm-install':
    command   => '/usr/bin/npm install',
    cwd       => $codedir,
    logoutput => on_failure,
  }

  exec { 'bower-install':
    command   => '/usr/bin/bower install --allow-root',
    cwd       => $codedir,
    require   => [Exec['npm-install']],
    onlyif    => [ "/usr/bin/bower list | tail -n +2" ],
    logoutput => on_failure,
  }

  class { 'postgresql::server': }
  postgresql::server::role { 'jotter':
    password_hash => postgresql_password('jotter', 'xoeNgee6'),
  } ->
  postgresql::server::database { 'jotter':
    owner => 'jotter',
  } ->
  postgresql::server::database_grant { 'jotter':
    privilege => 'ALL',
    db        => 'jotter',
    role      => 'jotter',
  } ->
  exec { 'initialize-database':
    command => '/usr/bin/python3 server/manage.py syncdb --noinput',
    cwd     => $codedir,
    require => Exec['pip-install'],
  } ->
  exec { 'migrate-database':
    command => '/usr/bin/python3 server/manage.py migrate',
    cwd     => $codedir,
  }
}
