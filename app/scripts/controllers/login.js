'use strict()';

jotterApp.controller('LoginCtrl',
['$location', '$scope', 'Session',
function ($location, $scope, Session) {
  $scope.password = '';
  $scope.username = '';

  Session.getUser({
    onSuccess: function (user) {
      if (user.isAuthenticated) {
        $location.path('/#/');
      }
    }
  });

  $scope.login = function () {
    Session.create(
      {
        password: $scope.password,
        username: $scope.username
      },
      function (response) { // success
        $scope.$root.$broadcast(
          'alert',
          {
            status: 'success',
            title: 'Welcome Back!'
          }
        );
        $location.path('/#/');
      }
    );
  };
}]);
