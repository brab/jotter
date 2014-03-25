'use strict()';

describe('Service: Budget', function () {
  var $httpBackend,
      Budget,
      resource;

  var budgets = [
    { 'id': 'b0001',
      'title': 'Test Budget'
    }
  ];

  beforeEach(module('jotterServices'));

  beforeEach(
    // jshint camelcase: false
    inject(function (_$httpBackend_, _Budget_) {
      $httpBackend = _$httpBackend_;
      Budget = _Budget_;
    })
  );

  afterEach(function () {
    resource = undefined;
    $httpBackend.verifyNoOutstandingExpectation();
    $httpBackend.verifyNoOutstandingRequest();
  });

  it('should load', function () {
    expect(Budget).toBeDefined();
  });

  describe('query()', function () {
    it('should make a GET request to the api', function () {
      $httpBackend.expectGET('/api/v1/budgets')
        .respond(200, budgets);

      Budget.query();

      $httpBackend.flush();
    });
  });

  describe('get()', function () {
    it('should make a GET request to the api', function () {
      $httpBackend.expectGET('/api/v1/budgets/b0001')
        .respond(200, budgets[0]);

      Budget.get({ id: 'b0001' });

      $httpBackend.flush();
    });
  });

  describe('save()', function () {
    it('should make a POST request to the api', function () {
      $httpBackend.expectPOST('/api/v1/budgets')
        .respond(200, budgets[0]);

      resource = Budget.save({ title: 'Test Budget' });

      $httpBackend.flush();

      expect(resource).toMatch(budgets[0]);
    });
  });
});
