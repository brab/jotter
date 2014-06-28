'use strict()';

jotterServices.factory('Budget', ['$resource', function ($resource) {
  var budgetResource = $resource(
    '/api/v1/budgets/:id',
    { id: '@id' },
    {
      query: {
        method: 'GET',
        params: {id: ''},
        isArray: true
      }
    }
  );

  var calculateTotals = function(budget) {
    // jshint camelcase: false
    budget.spent = 0;
    budget.amount = 0;
    _.each(budget.budget_categories, function(category) {
      budget.amount = budget.amount + category.amount;
      category.spent = 0;
      _.each(category.budget_expenses, function(expense) {
        category.spent = category.spent + expense.amount;
      });
      budget.spent = budget.spent + category.spent;
    });

    return budget;
  };

  return {
    get: function(args) {
      args = args || {};
      args.callbacks = args.callbacks || {};

      return budgetResource.get(
        {
          id: args.id
        },
        function(response) { //success
          calculateTotals(response);

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
    },

    query: function(args) {
      args = args || {};
      args.callbacks = args.callbacks || {};

      return budgetResource.query(
        function(response) { //success
          _.each(response, function(budget) {
            calculateTotals(budget);
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
    },

    save: function(args) {
      args = args || {};
      args.callbacks = args.callbacks || {};

      var budget = _.omit(args, 'callbacks');

      return budgetResource.save(
        budget,
        function(response) { //success
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
    }
  };
}]);
