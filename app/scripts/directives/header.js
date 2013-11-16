'use strict()';

jotterDirectives.directive('jtrHeader',
['$location', 'Session',
function ($location, Session) {
  return {
    restrict: 'E',
    scope: true,
    templateUrl: 'templates/header.html',
    link: function postLink (scope, element, attrs) {
      Session.getUser({
        onSuccess: function (user) {
          scope.user = user;
          if (!user.isAuthenticated) {
            $location.path('/login');
          }
        }
      });
    }
  };
}]);
