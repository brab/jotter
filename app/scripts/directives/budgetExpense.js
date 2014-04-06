'use strict()';

jotterDirectives.directive('jtrBudgetExpenseEdit', [function() {
  return {
    restrict: 'E',
    replace: true,
    scope: {
      expense : '='
    },
    templateUrl: 'templates/budgetExpense.html',
    link: function postLink(scope, element, attrs) {
      scope.$watch('expense.amountDollars', function(newVal, oldVal) {
        if(angular.isDefined(newVal) &&
           ('' + newVal).length > 0) {
          scope.expense.amount = +newVal * 100 || 0;
        }
      });
    }
  };
}]);
