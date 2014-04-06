'use strict()';

jotterServices.factory('BudgetExpense', ['$resource',
function ($resource) {
  var budgetExpenseResource = $resource('/api/v1/budget-expenses/:id',
    { id: '@id' },
    {
      update: { method: 'PUT' }
    }
  );

  return {
    save: function(args, callbacks) {
      // jshint camelcase: false
      args = args || {};
      args.budget_category = args.budget_category || {};
      callbacks = callbacks || args.callbacks || {};

      var budgetExpense = new budgetExpenseResource({
        amount: args.amount,
        budget_category: args.budget_category.id,
        id: args.id,
        title: args.title
      });

      if(angular.isDefined(args.id)) {
        budgetExpense.$update(
          function(response) { //success
            if(angular.isFunction(callbacks.onSuccess)) {
              callbacks.onSuccess(response);
            }
          },
          function(response) { //error
            if(angular.isFunction(callbacks.onError)) {
              callbacks.onError(response);
            }
          }
        );
      } else {
        budgetExpense.$save(
          function(response) { //success
            if(angular.isFunction(callbacks.onSuccess)) {
              callbacks.onSuccess(response);
            }
          },
          function(response) { //error
            if(angular.isFunction(callbacks.onError)) {
              callbacks.onError(response);
            }
          }
        );
      }

      return budgetExpense;
    }
  };
}]);
