'use strict()';

// Move controllers to their own module in app.js so that they don't depend
// on libraries like ngAnimate to test, just like Services + Directives
xdescribe('CheckListCtrl', function () {
  var $scope;
  var CheckListCtrl;

  beforeEach(module('jotterApp'));

  beforeEach(
    // jshint camelcase: false
    inject(function (_$rootScope_, $controller) {
      $scope = _$rootScope_.$new();

      CheckListCtrl = $controller('CheckListCtrl', { $scope: $scope });
    })
  );

  it ('should load', function () {
    //vars
    expect($scope.checkList).toBeDefined();
    expect($scope.checkListItemEdit).toBeDefined();

    //methods
    expect($scope.saveCheckListItem).toBeDefined();
    expect($scope.toggleCheckListItemChecked).toBeDefined();
  });
});
