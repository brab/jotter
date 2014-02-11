class prod_server {
  group { 'jotter':
    ensure => present,
  }

  user { 'jotter':
    ensure     => present,
    shell      => '/bin/bash',
    gid        => 'jotter',
    groups     => ['adm', 'sudo'],
    home       => '/home/jotter',
    managehome => true,
  }

  $packages_prod = [
    'apache2',
    'libapache2-mod-wsgi-py3',
  ]

  package { 'install-packages-prod':
    name    => $packages_prod,
    ensure  => 'installed',
    require => File['python-symlink'],
  }

  file { 'jotter/.ssh':
    path    => '/home/jotter/.ssh',
    ensure  => directory,
    owner   => 'jotter',
    require => User['jotter'],
    before  => [File['deploy_key', 'deploy_key_pub']],
  }

  file { 'ssh-config':
    path   => '/home/jotter/.ssh/config',
    source => 'puppet:///modules/prod_server/config',
    owner   => 'jotter',
    mode   => 644,
  }

  file { 'known_hosts':
    path   => '/home/jotter/.ssh/known_hosts',
    source => 'puppet:///modules/prod_server/known_hosts',
    owner   => 'jotter',
    mode   => 644,
  }

  file { 'deploy_key':
    path   => '/home/jotter/.ssh/id_rsa',
    source => 'puppet:///modules/prod_server/id_rsa',
    ensure => present,
    owner  => 'jotter',
    group  => 'jotter',
    mode   => 400,
    before => Exec['clone-repo'],
  }

  file { 'deploy_key_pub':
    path   => '/home/jotter/.ssh/id_rsa.pub',
    source => 'puppet:///modules/prod_server/id_rsa.pub',
    ensure => present,
    owner  => 'jotter',
    group  => 'jotter',
    mode   => 400,
    before => Exec['clone-repo'],
  }

  file { 'www-permissions':
    path   => '/var/www',
    ensure => directory,
    mode   => 757,
    before => Exec['clone-repo'],
  }

  exec { 'clone-repo':
    cwd     => '/var/www',
    command => '/usr/bin/git clone git@github.com:brab/jotter.git',
    user    => 'jotter',
    creates => '/var/www/jotter/',
    require => Package['install-packages'],
    before  => [
      Exec['pip-install-0'],
      Exec['gem-install'], 
      Exec['npm-install-global'],
      Exec['npm-install'],
      Exec['bower-install'],
    ]
  }

  file { 'wsgi-conf':
    path    => '/etc/apache2/sites-available/jotter',
    ensure  => link,
    target  => '/var/www/jotter/server/server/wsgi.conf',
    require => [Exec['clone-repo'], Package['install-packages-prod'],],
  }

  exec { 'apache-disable-default':
    command => '/usr/sbin/a2dissite 000-default',
  }

  exec { 'apache-enable-jotter':
    command => '/usr/sbin/a2ensite jotter',
    require => File['wsgi-conf'],
  }

  exec { 'apache-reload':
    command => '/usr/sbin/service apache2 reload',
    require => [Exec['apache-enable-jotter'], Exec['apache-disable-default'],],
  }
}
