'use strict';


// Declare app level module which depends on filters, and services
angular.module('recipeBook', ['recipeBook.filters', 'recipeBook.services', 'recipeBook.directives'])
  .config(['$routeProvider', '$locationProvider', function($routeProvider, $locationProvider) {
    $routeProvider
      .when('/home', {templateUrl: 'partials/home.html', controller: HomeCtrl})
      .when('/user', {templateUrl: 'partials/user.html', controller: UserDetailCtrl})

      .when('/recipes', { templateUrl: 'partials/recipe-list.html',
                          controller: RecipeListCtrl})
      .when('/recipes/:recipeId', { templateUrl: 'partials/recipe-detail.html',
                                    controller: RecipeDetailCtrl})
      
      .when('/shopping', { templateUrl: 'partials/shopping-list.html',
                           controller: ShoppingListCtrl})
      
      .otherwise({redirectTo: '/home'})
    ;
    //$locationProvider.html5Mode(true); //TODO: I'd love to get this working.
  }])
;
