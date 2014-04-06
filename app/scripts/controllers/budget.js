'use strict()';

jotterApp.controller('BudgetCtrl',
['$location', '$routeParams', '$scope', 'Budget', 'BudgetCategory', 'BudgetExpense', 'Session', 'User',
function($location, $routeParams, $scope, Budget, BudgetCategory, BudgetExpense, Session, User) {
  $scope.budgetCategoryEdit = {};
  $scope.budgetExpenseEdit = {};

  Session.getUser({
    onSuccess: function(user) {
      $scope.user = user;
    }
  });

  User.query(function(users) {
    $scope.users = _.reject(users, function(user) { return user.username === '!'; });
  });

  var budgetId = $routeParams.id;
  if(angular.isUndefined(budgetId) ||
      budgetId === '') {
    $scope.$root.$broadcast('alert', {
      title: "I can't find that budget"
    });
    $location.$path('/');
  }

  var loadBudget = function() {
    $scope.budget = Budget.get({ id: budgetId });
  };

  loadBudget();

  $scope.$on('budget:refresh', function() {
    loadBudget();
  });

  $scope.cancelBudgetCategoryEdit = function () {
    $scope.budgetCategoryEdit = {};
  };

  var saveNewBudgetCategory = function() {
    var newBudgetCategory = new BudgetCategory({
      // jshint camelcase: false
      amount: $scope.budgetCategoryEdit.amount,
      budget: $scope.budget.id,
      title: $scope.budgetCategoryEdit.title
    });
    var successFn = function() {
      // jshint camelcase: false
      $scope.budget.budget_categories.push(newBudgetCategory);
      $scope.budgetCategoryEdit.amount = '';
      $scope.budgetCategoryEdit.title = '';
    };
    var errorFn = function() {
      $scope.$root.$broadcast('alert', {
        message: "and we can't save " + $scope.budgetCategoryEdit.title + " right now",
        status: 'danger',
        title: "Something's wrong"
      });
    };
    newBudgetCategory.$save(successFn, errorFn);
  };

  $scope.saveBudgetCategory = function() {
    if(angular.isDefined($scope.budgetCategoryEdit.id)) {
      var budgetCategory = new BudgetCategory($scope.budgetCategoryEdit);
      budgetCategory.$update();
    } else {
      saveNewBudgetCategory();
    }
  };

  $scope.saveBudgetExpense = function() {
    BudgetExpense.save($scope.budgetExpenseEdit, {
      onSuccess: function(response) {
        // jshint camelcase: false
        var budgetCategory = $scope.budgetExpenseEdit.budget_category;
        budgetCategory.budget_expenses.push(response);
        budgetCategory.spent = budgetCategory.spent + response.amount;
      }
    });
  };

  $scope.editBudgetExpense = function(budgetExpense) {
    budgetExpense = budgetExpense || {};
    $scope.budgetExpenseEdit = budgetExpense;
  };

  $scope.$watch('budgetCategoryEdit.amountDollars', function(newVal, oldVal) {
    if(angular.isDefined(newVal) &&
       ('' + newVal).length > 0) {
      $scope.budgetCategoryEdit.amount = +newVal * 100 || 0;
    }
  });
}]);
