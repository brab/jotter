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
      };

      scope.editCheckListItem = function (checkListItem) {
        scope.checkListItemEdit = checkListItem;
        scope.showCheckListItemEditForm = true;
        checkListItem.showTools = false;
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
    }
  };
}]);
