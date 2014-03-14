'use strict()';

describe('Service: User', function () {
  var $httpBackend;
  var User;
  var resource;

  var users = [
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
    inject(function (_$httpBackend_, _User_) {
      $httpBackend = _$httpBackend_;
      User = _User_;
    })
  );

  afterEach(function () {
    resource = undefined;
    $httpBackend.verifyNoOutstandingExpectation();
    $httpBackend.verifyNoOutstandingRequest();
  });

  it('should load', function () {
    expect(User).toBeDefined();
  });

  describe('query()', function () {
    it('should make a GET request to the api', function () {
      $httpBackend.expectGET('/api/v1/users')
        .respond(200, users);

      User.query();

      $httpBackend.flush();
    });
  });

  describe('get()', function () {
    it('should make a GET request to the api', function () {
      $httpBackend.expectGET('/api/v1/users/u0001')
        .respond(200, users[0]);

      User.get({ id: 'u0001' });

      $httpBackend.flush();
    });
  });
});
