'use strict()';

jotterApp.controller('CheckListCtrl',
['$location', '$routeParams', '$scope', 'CheckList', 'CheckListItem', 'Session', 'User',
function($location, $routeParams, $scope, CheckList, CheckListItem, Session, User) {
  $scope.checkListItemEdit = {};

  Session.getUser({
    onSuccess: function(user) {
      $scope.user = user;
    }
  });

  User.query(function(users) {
    $scope.users = _.reject(users, function(user) { return user.username === '!'; });
  });

  var checkListId = $routeParams.id;
  if(angular.isUndefined(checkListId) ||
      checkListId === '') {
    $scope.$root.$broadcast('alert', {
      title: "I can't find that list"
    });
    $location.$path('/#/lists');
  }

  $scope.$on('checkList:refresh', function() {
    $scope.checkList = CheckList.get({ id: checkListId });
  });
  $scope.checkList = CheckList.get({ id: checkListId });

  var saveNewCheckListItem = function() {
    var newCheckListItem = new CheckListItem({
      // jshint camelcase: false
      check_list: $scope.checkList.id,
      checked: true,
      description: $scope.checkListItemEdit.description,
      title: $scope.checkListItemEdit.title
    });
    var successFn = function() {
      // jshint camelcase: false
      $scope.checkList.check_list_items.push(newCheckListItem);
      $scope.checkListItemEdit.description = '';
      $scope.checkListItemEdit.title = '';
    };
    var errorFn = function() {
      $scope.$root.$broadcast('alert', {
        message: "and we can't save " + $scope.checkListItemEdit.title + " right now",
        status: 'danger',
        title: "Something's wrong"
      });
    };
    newCheckListItem.$save(successFn, errorFn);
  };

  $scope.saveCheckListItem = function() {
    if(angular.isDefined($scope.checkListItemEdit.id)) {
      var checkListItem = new CheckListItem($scope.checkListItemEdit);
      checkListItem.$update();
    } else {
      saveNewCheckListItem();
    }
  };

  $scope.toggleCheckListItemChecked = function(checkListItem) {
    checkListItem.checked = !checkListItem.checked;
    checkListItem = new CheckListItem(checkListItem);
    checkListItem.$update();
  };
}]);
