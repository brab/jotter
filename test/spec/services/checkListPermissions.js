'use strict()';

describe('Service: CheckListPermissions', function () {
  var $httpBackend,
      CheckListPermissions,
      resource;

  var checkListPermissions = [
    { 'id': 'u0001',
      'username': 'peterpan',
      'email': 'peterpan@jotter.ca',
      'password': 'HASHED'
    },
    { 'id': 'u0002',
      'username': 'wendydarling',
      'email': 'wendydarling@jotter.ca',
      'password': 'HASHED'
    }
  ];

  beforeEach(module('jotterServices'));

  beforeEach(
    // jshint camelcase: false
    inject(function (_$httpBackend_, _CheckListPermissions_) {
      $httpBackend = _$httpBackend_;
      CheckListPermissions = _CheckListPermissions_;
    })
  );

  afterEach(function () {
    resource = undefined;
    $httpBackend.verifyNoOutstandingExpectation();
    $httpBackend.verifyNoOutstandingRequest();
  });

  it('should load', function () {
    expect(CheckListPermissions).toBeDefined();
  });

  describe('query()', function () {
    it('should make a GET request to the api', function () {
      $httpBackend.expectGET('/api/v1/check-list-permissions/cl0001')
        .respond(200, checkListPermissions);

      CheckListPermissions.query({ id: 'cl0001' });

      $httpBackend.flush();
    });
  });

  describe('toggle()', function () {
    it('should make a PUT request to the api', function () {
      $httpBackend.expectPUT('/api/v1/check-list-permissions/cl0001')
        .respond(200, checkListPermissions[0]);

      resource = CheckListPermissions.toggle({ id: 'cl0001', user: 1 });

      $httpBackend.flush();
    });
  });
});
