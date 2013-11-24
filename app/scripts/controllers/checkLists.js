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

  $scope.getNumChecked = function (checkList) {
    if (angular.isUndefined(checkList)) { return 0; }
    return _.size(_.where(checkList.check_list_items,  { checked: true }));
  };
}]);
