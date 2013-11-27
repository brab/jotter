'use strict()';

jotterApp.controller('CheckListCtrl',
['$location', '$routeParams', '$scope', 'CheckList', 'CheckListItem', 'Session',
function ($location, $routeParams, $scope, CheckList, CheckListItem, Session) {
  $scope.checkListItemEdit = {};

  Session.getUser({
    onSuccess: function (user) {
      $scope.user = user;
    }
  });

  var checkListId = $routeParams.id;
  if (angular.isUndefined(checkListId) ||
      checkListId === '') {
    $scope.$root.$broadcast('alert', {
      title: "I can't find that list"
    });
    $location.$path('/#/lists');
  }

  $scope.checkList = CheckList.get({ id: checkListId });

  var saveNewCheckListItem = function () {
    var newCheckListItem = new CheckListItem({
      // jshint camelcase: false
      check_list: $scope.checkList.id,
      checked: false,
      description: $scope.checkListItemEdit.description,
      title: $scope.checkListItemEdit.title
    });
    var successFn = function () {
      // jshint camelcase: false
      $scope.checkList.check_list_items.push(newCheckListItem);
      $scope.checkListItemEdit.description = '';
      $scope.checkListItemEdit.title = '';
    };
    var errorFn = function () {
      $scope.$root.$broadcast('alert', {
        message: "and we can't save " + $scope.checkListItemEdit.title + " right now",
        status: 'danger',
        title: "Something's wrong"
      });
    };
    newCheckListItem.$save(successFn, errorFn);
  };

  $scope.saveCheckListItem = function () {
    if (angular.isDefined($scope.checkListItemEdit.id)) {
      $scope.checkListItemEdit.$update();
    } else {
      saveNewCheckListItem();
    }
  };
}]);
