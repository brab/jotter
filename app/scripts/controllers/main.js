'use strict()';

jotterApp.controller('MainCtrl', ['$location', '$scope', 'CheckList', 'Session',
function($location, $scope, CheckList, Session) {
  Session.getUser({
    onSuccess: function(user) {
      $scope.user = user;
    }
  });

  $scope.checkListEdit = {};
  $scope.checkLists = CheckList.query();

  $scope.getNumChecked = function(checkList) {
    if(angular.isUndefined(checkList)) { return 0; }
    return _.size(_.where(
      // jshint camelcase: false
      checkList.check_list_items,
      { checked: true }
    ));
  };

  var saveNewCheckList = function() {
    var newCheckList = new CheckList($scope.checkListEdit);
    var successFn = function() {
      $scope.checkLists.unshift(newCheckList);
      $scope.newCheckListTitle = '';
    };
    var errorFn = function() {
      $scope.$root.$broadcast('alert', {
        message: "and we can't save " + $scope.newCheckListTitle + " right now",
        status: 'danger',
        title: "Something's wrong"
      });
    };
    newCheckList.$save(successFn, errorFn);
  };

  $scope.saveCheckList = function() {
    if(angular.isDefined($scope.checkListEdit.id)) {
      var checkList = new CheckList($scope.checkListEdit);
      checkList.$update();
    } else {
      saveNewCheckList();
    }
  };
}]);
