'use strict()';

jotterApp.controller('MainCtrl', ['$scope', 'CheckList',
function ($scope, CheckList) {
  $scope.checkLists = CheckList.query();
}]);
