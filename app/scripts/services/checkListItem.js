'use strict()';

jotterServices.factory('CheckListItem', ['$resource',
function ($resource) {
  return $resource('/api/v1/check-list-items/:id',
    { id: '@id' },
    {
      update: { method: 'PUT' }
    }
  );
}]);
