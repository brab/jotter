'use strict()';

jotterDirectives.directive('jtrAlert', ['$timeout', function ($timeout) {
  // Alerts are triggered by an event on the scope
  //
  // $rootScope.$broadcast('alert', args);
  // args:
  //  status  <string> info|success|warning|danger
  //  title   <string>
  //  message <string>
  return {
    restrict: 'E',
    scope: true,
    templateUrl: 'templates/alert.html',
    link: function postLink (scope, element, attrs) {
      // vars
      scope.alertStatus = 'alert-info';
      scope.message = '';
      scope.title = '';
      scope.visible = false;

      // watchers
      scope.$on('alert', function (event, args) {
        scope.alertStatus = 'alert-' + (args.status || 'info');
        scope.message = args.message;
        scope.title = args.title;
        scope.visible = true;

        $timeout(function () {
          scope.dismiss();
        }, 6500);
      });

      // scope methods
      scope.dismiss = function () {
        scope.visible = false;
      };
    }
  };
}]);
