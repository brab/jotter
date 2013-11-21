'use strict()';

jotterApp.controller('CheckListsCtrl',
['$scope', 'CheckList', 'Session',
function ($scope, CheckList, Session) {
  Session.getUser({
    onSuccess: function (user) {
      $scope.user = user;
    }
  });

  $scope.checkLists = CheckList.query();
}]);
