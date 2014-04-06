'use strict()';

jotterServices.factory('Budget', ['$resource', function ($resource) {
  var budgetResource = $resource('/api/v1/budgets/:id',
    { id: '@id' },
    {
      query: {
        method: 'GET',
        params: {id: ''},
        isArray: true
      }
    }
  );

  return {
    get: function(args) {
      args = args || {};
      args.callbacks = args.callbacks || {};

      var resource = budgetResource.get(
        {
          id: args.id
        },
        function(response) { //success
          // jshint camelcase: false
          response.spent = 0;
          _.each(response.budget_categories, function(category) {
            category.spent = 0;
            _.each(category.budget_expenses, function(expense) {
              category.spent = category.spent + expense.amount;
            });
            response.spent = response.spent + category.spent;
          });

          if(angular.isFunction(args.callbacks.onSuccess)) {
            args.callbacks.onSuccess(response);
          }
        },
        function(response) { //error
          if(angular.isFunction(args.callbacks.onError)) {
            args.callbacks.onError(response);
          }
        }
      );
      return resource;
    }
  };
}]);
