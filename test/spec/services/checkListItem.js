'use strict()';

describe('Service: CheckListItem', function () {
  var $httpBackend,
      CheckListItem,
      resource;

  var checkListItems = [
    { 'id': 'cli0001',
      'check_list': 'cl0001',
      'checked': false,
      'title': 'Thing 1',
      'description': 'Something about thing 1'
    },
    { 'id': 'cli0002',
      'check_list': 'cl0001',
      'checked': true,
      'title': 'Thing 2',
      'description': 'Something about thing 2'
    }
  ];

  beforeEach(module('jotterServices'));

  beforeEach(
    // jshint camelcase: false
    inject(function (_$httpBackend_, _CheckListItem_) {
      $httpBackend = _$httpBackend_;
      CheckListItem = _CheckListItem_;
    })
  );

  afterEach(function () {
    resource = undefined;
    $httpBackend.verifyNoOutstandingExpectation();
    $httpBackend.verifyNoOutstandingRequest();
  });

  it('should load', function () {
    expect(CheckListItem).toBeDefined();
  });

  describe('delete()', function () {
    it('should make a DELETE request when passed arguments', function () {
      $httpBackend.expectDELETE('/api/v1/check-list-items/cli0001')
        .respond(204);

      resource = CheckListItem.delete({
        id: 'cli0001'
      });

      $httpBackend.flush();
    });

    it('should make a DELETE request when called on an instance', function () {
      $httpBackend.expectDELETE('/api/v1/check-list-items/cli0001')
        .respond(204);

      var checkListItem = new CheckListItem({
        check_list: 'cl0001',
        checked: false,
        id: 'cli0001',
        title: 'Thing 1',
        description: 'Something about thing 1'
      });

      checkListItem.$delete();
      $httpBackend.flush();
    });
  });

  describe('save()', function () {
    it('should make a POST request when passed arguments', function () {
      $httpBackend.expectPOST('/api/v1/check-list-items')
        .respond(200, checkListItems[0]);

      resource = CheckListItem.save({
        check_list: 'cl0001',
        checked: false,
        title: 'Thing 1',
        description: 'Something about thing 1'
      });

      $httpBackend.flush();

      expect(resource.id).toEqual(checkListItems[0].id);
    });

    it('should make a POST request when called on an instance', function () {
      $httpBackend.expectPOST('/api/v1/check-list-items')
        .respond(200, checkListItems[0]);

      var checkListItem = new CheckListItem({
        check_list: 'cl0001',
        checked: false,
        title: 'Thing 1',
        description: 'Something about thing 1'
      });

      checkListItem.$save();
      $httpBackend.flush();
      expect(checkListItem.id).toEqual(checkListItems[0].id);
    });
  });

  describe('update()', function () {
    it('should make a PUT request when passed arguments', function () {
      $httpBackend.expectPUT('/api/v1/check-list-items/cli0001')
        .respond(200, checkListItems[0]);

      resource = CheckListItem.update({
        check_list: 'cl0001',
        checked: false,
        id: 'cli0001',
        title: 'Thing 1',
        description: 'Something about thing 1'
      });

      $httpBackend.flush();

      expect(resource.id).toEqual(checkListItems[0].id);
    });

    it('should make a PUT request when called on an instance', function () {
      $httpBackend.expectPUT('/api/v1/check-list-items/cli0001')
        .respond(200, checkListItems[0]);

      var checkListItem = new CheckListItem({
        check_list: 'cl0001',
        checked: false,
        id: 'cli0001',
        title: 'Thing 1',
        description: 'Something about thing 1'
      });

      checkListItem.$update();
      $httpBackend.flush();
      expect(checkListItem.id).toEqual(checkListItems[0].id);
    });
  });
});
