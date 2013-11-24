'use strict()';

var jotterDirectives = angular.module('jotterDirectives', []);
var jotterServices = angular.module('jotterServices', ['ngResource']);

var jotterApp = angular.module('jotterApp',
    ['jotterDirectives', 'jotterServices', 'jotterTemplates', 'ngAnimate', 'ngRoute'])
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
      .when('/login', {
        templateUrl: 'static/views/login.html',
        controller: 'LoginCtrl'
      })
      .otherwise({
        redirectTo: '/'
      });
  })
  
  .config(function ($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
  });
