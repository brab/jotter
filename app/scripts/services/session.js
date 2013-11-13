'use strict()';

jotterServices.factory('Session', ['$resource',
function ($resource) {
  return $resource('/api/v1/sessions\\/',
    {},
    {
      create: { method: 'POST' },
      //get: { method: 'GET' }
    }
  );
}]);
