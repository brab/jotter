'use strict()';

describe('Service: BudgetExpense', function () {
  var $httpBackend,
      BudgetExpense,
      resource;

  var budgetExpenses = [
    {
      amount: 10000,
      id: 'be0001',
      title: 'Cookies'
    }
  ];

  beforeEach(module('jotterServices'));

  beforeEach(
    // jshint camelcase: false
    inject(function (_$httpBackend_, _BudgetExpense_) {
      $httpBackend = _$httpBackend_;
      BudgetExpense = _BudgetExpense_;
    })
  );

  afterEach(function () {
    resource = undefined;
    $httpBackend.verifyNoOutstandingExpectation();
    $httpBackend.verifyNoOutstandingRequest();
  });

  it('should load', function () {
    expect(BudgetExpense).toBeDefined();
  });

  describe('save()', function () {
    describe('with a new budget expense', function() {
      it('should make a POST request to the api', function () {
        $httpBackend.expectPOST('/api/v1/budget-expenses')
          .respond(200, budgetExpenses[0]);

        resource = BudgetExpense.save({
          amount: 10000,
          title: 'Cookies'
        });

        $httpBackend.flush();

        expect(resource).toMatch(budgetExpenses[0]);
      });
    });

    describe('with an existing budget expense', function() {
      it('should make a PUT request to the api', function() {
        $httpBackend.expectPUT('/api/v1/budget-expenses/be0001')
          .respond(200, budgetExpenses[0]);

        resource = BudgetExpense.save(budgetExpenses[0]);

        $httpBackend.flush();

        expect(resource).toMatch(budgetExpenses[0]);
      });
    });
  });
});
