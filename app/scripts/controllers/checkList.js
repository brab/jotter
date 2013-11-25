'use strict()';

jotterApp.controller('CheckListCtrl',
['$location', '$routeParams', '$scope', 'CheckList', 'Session',
function ($location, $routeParams, $scope, CheckList, Session) {
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

}]);
