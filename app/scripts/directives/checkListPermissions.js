'use strict()';

jotterDirectives.directive('jtrCheckListPermissions',
['$timeout', 'CheckListPermissions', function($timeout, CheckListPermissions) {
  return {
    restrict: 'A',
    link: function postLink(scope, element, attrs) {
      scope.showCheckListPermissionsEditForm = false;
      scope.checkListPermissions = [ ];
      scope.checkListPermissionsSelect2Options = {
        placeholder:'type to search',
        width: 'resolve'
      };

      var loadPermissions = function() {
        if(!scope.checkList.$resolved || scope.users.length < 1) {
          $timeout(function() {
            loadPermissions();
          }, 100);
        }
        scope.checkListPermissions = CheckListPermissions.query(
          { id: scope.checkList.id },
          function(permUsers) {
            var user;
            _.each(permUsers, function(permUser) {
              user = _.findWhere(scope.users, { username: permUser.username });
              if(angular.isDefined(user)) {
                user.hasPermissions = true;
              }
            });
            var owner = _.findWhere(scope.users, { username: scope.user.username });
            owner.locked = true;
            $timeout(function() {
              element.find('#checkListPermissionsEditUsers')
                .select2(scope.checkListPermissionsSelect2Options)
                .on('change', function(data) {
                  scope.toggleCheckListPermission(data.added || data.removed);
                });
            }, 50);
          }
        );
      };

      scope.cancelCheckListPermissionsEdit = function() {
        scope.showCheckListPermissionsEditForm = false;
      };

      scope.editCheckListPermissions = function() {
        if(scope.checkListPermissions.length === 0) {
          loadPermissions();
        }
        scope.showCheckListPermissionsEditForm = true;
      };

      scope.toggleCheckListPermission = function(user) {
        CheckListPermissions.toggle({
          id: scope.checkList.id,
          user: user.id
        });
      };
    }
  };
}]);
