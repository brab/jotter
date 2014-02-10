'use strict()';

jotterApp.controller('CheckListsCtrl',
['$location', '$scope', 'CheckList', 'Session',
function ($location, $scope, CheckList, Session) {
  $scope.newCheckListTitle = '';

  Session.getUser({
    onSuccess: function (user) {
      $scope.user = user;
    }
  });

  $scope.checkLists = CheckList.query();

  $scope.getNumChecked = function (checkList) {
    if (angular.isUndefined(checkList)) { return 0; }
    return _.size(_.where(
      // jshint camelcase: false
      checkList.check_list_items,
      { checked: true }
    ));
  };

  $scope.gotoList = function (checkList) {
    $location.path('/#/lists/' + checkList.id);
  };

  $scope.saveNewCheckList = function () {
    var newCheckList = new CheckList({ title: $scope.newCheckListTitle });
    var successFn = function () {
      $scope.checkLists.unshift(newCheckList);
      $scope.newCheckListTitle = '';
    };
    var errorFn = function () {
      $scope.$root.$broadcast('alert', {
        message: "and we can't save " + $scope.newCheckListTitle + " right now",
        status: 'danger',
        title: "Something's wrong"
      });
    };
    newCheckList.$save(successFn, errorFn);
  };
}]);
