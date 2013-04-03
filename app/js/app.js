'use strict';


// Declare app level module which depends on filters, and services
angular.module('recipeBook', ['recipeBook.filters', 'recipeBook.services', 'recipeBook.directives']).
  config(['$routeProvider', function($routeProvider) {
    $routeProvider
      .when('/home', {templateUrl: 'partials/home.html', controller: HomeCtrl})
      .when('/recipes', {templateUrl: 'partials/recipe-list.html', controller: RecipeListCtrl})
      .when('/shopping', {templateUrl: 'partials/shopping-list.html', controller: ShoppingListCtrl})
      .otherwise({redirectTo: '/home'});
  }]);
