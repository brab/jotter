'use strict()';

jotterServices.factory('Session', ['$resource',
function ($resource) {

  var User = function () {
    var isAuthenticated = false;
    var isSet = false;
    var username = '';

    return {
      isAuthenticated: isAuthenticated,
      isSet: isSet,
      username: username,

      setFromResource: function (resource) {
        this.isAuthenticated = resource.isAuthenticated;
        this.isSet = true;
        this.username = resource.username;
      }
    };
  };
  var currentUser = User();

  var sessionResource = $resource('/api/v1/sessions',
    {},
    {
      create: { method: 'POST' },
      delete: { method: 'DELETE' },
      get: { method: 'GET' }
    }
  );

  return {
    create: function () {
      var args = arguments[0] || {};
      var successCallback = arguments[1] || function () {};
      var errorCallback = arguments[2] || function () {};

      var onSuccess = function (resource) {
        currentUser.setFromResource(resource);
        successCallback(resource);
      };
      var onError = function (resource) {
        errorCallback(resource);
      };
      sessionResource.create(args, onSuccess, onError);
    },

    delete: function () {
      var successCallback = arguments[1] || function () {};
      var errorCallback = arguments[2] || function () {};

      var onSuccess = function (resource) {
        currentUser.setFromResource(resource);
        successCallback(resource);
      };
      var onError = function (resource) {
        errorCallback(resource);
      };
      sessionResource.delete(onSuccess, onError);
    },

    getUser: function (callbacks) {
      callbacks = callbacks || {};
      if (! currentUser.isSet) {
        sessionResource.get(
          {},
          function (resource) {
            currentUser.setFromResource(resource);
            if (angular.isFunction(callbacks.onSuccess)) {
              callbacks.onSuccess(currentUser);
            }
          }
        );
      } else {
        if (angular.isFunction(callbacks.onSuccess)) {
          callbacks.onSuccess(currentUser);
        }
      }
    }
  };
}]);
