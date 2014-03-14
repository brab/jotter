'use strict()';

jotterServices.factory('User', ['$resource',
function ($resource) {
  return $resource('/api/v1/users/:id',
    { id: '@id' },
    {
      query: {
        method: 'GET',
        params: { id: '' },
        isArray: true
      }
    }
  );
}]);
