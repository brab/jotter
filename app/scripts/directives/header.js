'use strict()';

jotterDirectives.directive('jtrHeader', [function () {
  return {
    restrict: 'E',
    scope: true,
    templateUrl: 'templates/header.html',
    link: function postLink (scope, element, attrs) {
    }
  };
}]);
