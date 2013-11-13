'use strict()';

describe('Service: Session', function () {
  var $httpBackend,
      Session,
      resource;

  beforeEach(module('jotterServices'));

  beforeEach(
    // jshint camelcase: false
    inject(function (_$httpBackend_, _Session_) {
      $httpBackend = _$httpBackend_;
      Session = _Session_;
    })
  );

  afterEach(function () {
    resource = undefined;
    $httpBackend.verifyNoOutstandingExpectation();
    $httpBackend.verifyNoOutstandingRequest();
  });

  it('should load', function () {
    expect(Session).toBeDefined();
  });

  describe('delete()', function() {
    it('should make a DELETE request to the api', function () {
      $httpBackend.expectDELETE('/api/v1/sessions\\')
        .respond(204);

      Session.delete();

      $httpBackend.flush();
    });
  });

  describe('post()', function () {
    it('should make a POST request to the api', function () {
      $httpBackend.expectPOST('/api/v1/sessions\\')
        .respond(201);

      Session.create({
        'password': 'password',
        'username': 'test'
      });

      $httpBackend.flush();
    });
  });
});
