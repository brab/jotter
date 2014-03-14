'use strict()';

describe('Directive: jtrCheckListPermissions', function() {
  var $compile;
  //var $dscope;
  var $scope;
  var CheckListPermissions;
  var element;

  var compileElement = function() {
    element = angular.element('<div jtr-check-list-permissions></div>');

    $scope.checkList = {
      $resolved: true,
      id: 'cl0001'
    };
    $scope.users = [
      {
        id: 'u0001',
        username: 'peterpan'
      }
    ];

    $compile(element)($scope);
    $scope.$apply();
    // there are no child DOM elements
    //$dscope = element.children().scope();
  };

  beforeEach(module('jotterDirectives'));
  beforeEach(module('jotterServices'));

  beforeEach(
    // jshint camelcase: false
    inject(function(_$rootScope_, _$compile_, _CheckListPermissions_) {
      $scope = _$rootScope_.$new();
      $compile = _$compile_;
      CheckListPermissions = _CheckListPermissions_;

      spyOn(CheckListPermissions, 'query');
      spyOn(CheckListPermissions, 'toggle');
    })
  );

  it('should load', function() {
    compileElement();

    expect($scope.showCheckListPermissionsEditForm).toBeDefined();
    expect($scope.checkListPermissions).toBeDefined();
    expect($scope.checkListPermissionsSelect2Options).toBeDefined();
    expect($scope.closeCheckListPermissionsEdit).toBeDefined();
    expect($scope.editCheckListPermissions).toBeDefined();
    expect($scope.toggleCheckListPermission).toBeDefined();
  });

  describe('closeCheckListPermissionsEdit()', function() {
    it('should set showCheckListPermissionsEditForm to false', function() {
      compileElement();

      expect($scope.showCheckListPermissionsEditForm).toBeFalsy();

      $scope.showCheckListPermissionsEditForm = true;
      expect($scope.showCheckListPermissionsEditForm).toBeTruthy();

      $scope.closeCheckListPermissionsEdit();
      expect($scope.showCheckListPermissionsEditForm).toBeFalsy();
    });
  });

  describe('editCheckListPermissions()', function() {
    it('should set showCheckListPermissionsEditForm to true', function() {
      compileElement();

      expect($scope.showCheckListPermissionsEditForm).toBeFalsy();

      $scope.editCheckListPermissions();
      expect($scope.showCheckListPermissionsEditForm).toBeTruthy();
    });

    it('should call the CheckListPermissions service', function() {
      compileElement();

      $scope.editCheckListPermissions();

      expect(CheckListPermissions.query).toHaveBeenCalled();
    });
  });

  describe('toggleCheckListPermission', function() {
    it('should call the CheckListPermissions service', function() {
      compileElement();

      $scope.toggleCheckListPermission($scope.users[0]);

      expect(CheckListPermissions.toggle).toHaveBeenCalled();
    });
  });
});
