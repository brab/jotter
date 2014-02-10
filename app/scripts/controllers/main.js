'use strict()';

jotterApp.controller('MainCtrl', ['$location', '$scope', 'CheckList', 'Session',
function ($location, $scope, CheckList, Session) {
  Session.getUser({
    onSuccess: function (user) {
      $scope.user = user;
    }
  });

  $scope.checkLists = CheckList.query();

  $scope.gotoCheckList = function (checkList) {
    $location.path('/lists/' + checkList.id);
  };
}]);
