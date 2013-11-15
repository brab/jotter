'use strict()';

jotterApp.controller('LoginCtrl',
['$location', '$scope', 'Session',
function ($location, $scope, Session) {
  $scope.password = '';
  $scope.username = '';

  $scope.login = function () {
    Session.create(
      {
        password: $scope.password,
        username: $scope.username
      },
      function (response) { // success
        $location.path('/');
      }
    );
  };
}]);
