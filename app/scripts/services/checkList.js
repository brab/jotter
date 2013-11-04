'use strict()';

jotterServices.factory('CheckList', ['$resource',
function ($resource) {
  return $resource('/api/v1/check-lists\\/:id',
    {},
    {
      query: {
        method: 'GET',
        params: {id: ''},
        isArray: true
      }
    }
  );
}]);
