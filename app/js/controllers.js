'use strict';

/* Controllers */


function HomeCtrl() {
  
}

function RecipeListCtrl($scope, Recipe) {
  $scope.recipes = Recipe.query();
}

function RecipeDetailCtrl($scope, Recipe, $routeParams) {
  if ($routeParams.recipeId.toLowerCase() == 'new') {
    $scope.recipe = new Recipe();
    $scope.editMode = true;
  } else {
    $scope.recipe = Recipe.get({ recipeId: $routeParams.recipeId });
  }
  $scope.toggleEditMode = function() {
    $scope.editMode = !$scope.editMode;
  }
}

function ShoppingListCtrl() {
  
}
