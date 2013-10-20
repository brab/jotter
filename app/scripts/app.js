'use strict()';

var jotterServices = angular.module('jotterServices', ['ngResource']);

var jotterApp = angular.module('jotterApp', ['jotterServices', 'ngRoute'])
  .config(function ($routeProvider) {
    $routeProvider
      .when('/', {
        templateUrl: 'static/views/main.html',
        controller: 'MainCtrl'
      })
      .when('/lists', {
        templateUrl: 'static/views/checkLists.html',
        controller: 'CheckListsCtrl'
      })
      .otherwise({
        redirectTo: '/'
      });
  });
