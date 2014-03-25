'use strict()';

jotterApp.controller('MainCtrl',
['$location', '$scope', 'Budget', 'CheckList', 'Session',
function($location, $scope, Budget, CheckList, Session) {
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

  $scope.gotoCheckList = function(checkList) {
    $location.path('/lists/' + checkList.id);
  };

  var saveNewCheckList = function() {
    var newCheckList = new CheckList($scope.checkListEdit);
    var successFn = function() {
      $scope.checkLists.unshift(newCheckList);
    };
    var errorFn = function() {
      $scope.$root.$broadcast('alert', {
        message: "and we can't save " + $scope.checkListEdit.title + " right now",
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
    $scope.showCheckListEdit = false;
  };

  $scope.budgetEdit = {};
  $scope.budgets = Budget.query();

  $scope.gotoBudget = function(budget) {
    $location.path('/budgets/' + budget.id);
  };

  var saveNewBudget = function() {
    var newBudget = new Budget($scope.budgetEdit);
    var successFn = function() {
      $scope.budgets.unshift(newBudget);
    };
    var errorFn = function() {
      $scope.$root.$broadcast('alert', {
        message: "and we can't save " + $scope.budgetEdit.title + " right now",
        status: 'danger',
        title: "Something's wrong"
      });
    };
    newBudget.$save(successFn, errorFn);
  };

  $scope.saveBudget = function() {
    if(angular.isDefined($scope.budgetEdit.id)) {
      var budget = new Budget($scope.budgetEdit);
      budget.$update();
    } else {
      saveNewBudget();
    }
    $scope.showBudgetEdit = false;
  };
}]);
