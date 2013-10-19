'use strict()';

var jotterModule = angular.module('jotterModule', ['ngRoute'])
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
