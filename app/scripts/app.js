'use strict()';

var jotterDirectives = angular.module('jotterDirectives', []);
var jotterServices = angular.module('jotterServices', ['ngResource']);

var jotterApp = angular.module('jotterApp',
    ['jotterDirectives', 'jotterServices', 'jotterTemplates', 'ngAnimate', 'ngRoute', 'ngTouch', 'ui.select2'])
  .config(['$routeProvider', function ($routeProvider) {
    $routeProvider
      .when('/', {
        templateUrl: 'static/views/main.html',
        controller: 'MainCtrl'
      })
      .when('/lists', {
        templateUrl: 'static/views/checkLists.html',
        controller: 'CheckListsCtrl'
      })
      .when('/lists/:id', {
        templateUrl: 'static/views/checkList.html',
        controller: 'CheckListCtrl'
      })
      .when('/login', {
        templateUrl: 'static/views/login.html',
        controller: 'LoginCtrl'
      })
      .otherwise({
        redirectTo: '/'
      });
  }])
  
  .config(['$httpProvider', function ($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
  }]);
