'use strict';

/* Services */

angular.module('recipeBook.services', ['ngResource'])
  .factory('Recipe', function($resource) {
    return $resource('/recipes/:recipeId', { recipeId: '@id' });
  })
  .factory('User', function($resource) {
    return $resource('/user');
  })
;
