'use strict()';

describe('Service: CheckList', function () {
  var $httpBackend,
      CheckList,
      resource;

  var checkLists = [
    { 'id': 'cl0001',
      'title': 'Test List'
    }
  ];

  beforeEach(module('jotterServices'));

  beforeEach(
    // jshint camelcase: false
    inject(function (_$httpBackend_, _CheckList_) {
      $httpBackend = _$httpBackend_;
      CheckList = _CheckList_;
    })
  );

  afterEach(function () {
    resource = undefined;
    $httpBackend.verifyNoOutstandingExpectation();
    $httpBackend.verifyNoOutstandingRequest();
  });

  it('should load', function () {
    expect(CheckList).toBeDefined();
  });

  describe('query()', function () {
    it('should make a GET request to the api', function () {
      $httpBackend.expectGET('/api/v1/check-lists')
        .respond(200, checkLists);

      CheckList.query();

      $httpBackend.flush();
    });
  });

  describe('get()', function () {
    it('should make a GET request to the api', function () {
      $httpBackend.expectGET('/api/v1/check-lists/cl0001')
        .respond(200, checkLists[0]);

      CheckList.get({ id: 'cl0001' });

      $httpBackend.flush();
    });
  });

  describe('save()', function () {
    it('should make a POST request to the api', function () {
      $httpBackend.expectPOST('/api/v1/check-lists')
        .respond(200, checkLists[0]);

      resource = CheckList.save({ title: 'Test List' });

      $httpBackend.flush();

      expect(resource).toMatch(checkLists[0]);
    });
  });
});
