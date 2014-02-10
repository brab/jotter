Package { provider => 'apt', }

node 'local' {
  $codedir = '/home/vagrant/app'
  
  include 'stdlib'
  include 'general'
  include 'local_dev'
}

node 'prod' {
  $codedir = '/var/www/jotter'

  include 'stdlib'
  include 'prod_server'
  include 'general'
}
