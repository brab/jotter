'use strict()';

jotterServices.factory('Budget', ['$resource',
function ($resource) {
  return $resource('/api/v1/budgets/:id',
    { id: '@id' },
    {
      query: {
        method: 'GET',
        params: {id: ''},
        isArray: true
      }
    }
  );
}]);
