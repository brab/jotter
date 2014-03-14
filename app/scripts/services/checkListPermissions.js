'use strict()';

jotterServices.factory('CheckListPermissions', ['$resource',
function ($resource) {
  return $resource('/api/v1/check-list-permissions/:id',
    { id: '@id' },
    {
      'toggle': { method: 'PUT' }
    }
  );
}]);
