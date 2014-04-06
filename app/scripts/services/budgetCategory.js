'use strict()';

jotterServices.factory('BudgetCategory', ['$resource',
function ($resource) {
  return $resource('/api/v1/budget-categories/:id',
    { id: '@id' },
    {
      update: { method: 'PUT' }
    }
  );
}]);
