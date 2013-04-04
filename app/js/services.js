'use strict';

/* Services */


// Demonstrate how to register services
// In this case it is a simple value service.
angular.module('recipeBook.services', ['ngResource'])
  .factory('Recipe', function($resource) {
    return $resource('/recipes/:recipeId', { recipeId: '@id' });
  })
;
