'use strict()';

jotterDirectives.directive('jtrCheckListItems',
[function () {
  return {
    restrict: 'A',
    link: function postLink (scope, element, attrs) {
      scope.showCheckListItemEditForm = false;

      scope.cancelCheckListItemEdit = function () {
        scope.checkListItemEdit = {};
        scope.showCheckListItemEditForm = false;
        scope.$root.$broadcast('checkList:refresh');
      };

      scope.editCheckListItem = function (checkListItem) {
        scope.checkListItemEdit = checkListItem;
        scope.showCheckListItemEditForm = true;
        scope.hideCheckListItemTools(checkListItem);
      };

      scope.newCheckListItem = function () {
        scope.editCheckListItem({});
      };

      scope.hideCheckListItemTools = function (checkListItem) {
        checkListItem.showTools = false;
      };

      scope.showCheckListItemTools = function (checkListItem) {
        checkListItem.showTools = true;
      };

      scope.quickSaveCheckListItem = function() {
        scope.checkListItemEdit = {};
        scope.checkListItemEdit.title = angular.copy(scope.itemSearch);
        scope.itemSearch = '';
        scope.saveCheckListItem();
      };
    }
  };
}]);
