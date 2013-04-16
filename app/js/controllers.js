'use strict';

/* Controllers */


function HomeCtrl() {
  
}

function UserDetailCtrl($scope, User) {
  $scope.user = User.query(); //TODO: What if user is not logged in?
}

function RecipeListCtrl($scope, Recipe) {
  $scope.recipes = Recipe.query();
}

function RecipeDetailCtrl($scope, Recipe, $routeParams, $location) {
  if ($routeParams.recipeId.toLowerCase() == 'new') {
    $scope.recipe = new Recipe();
    $scope.editMode = true;
  } else {
    $scope.recipe = Recipe.get({ recipeId: $routeParams.recipeId });
  }
  $scope.toggleEditMode = function() {
    $scope.editMode = !$scope.editMode;
  };
  $scope.editRecipe = function() {
    $scope.originalRecipe = angular.copy($scope.recipe);
    $scope.editMode = true;
  };
  $scope.resetRecipe = function() {
    if ($scope.recipe.id) {
      $scope.recipe = angular.copy($scope.originalRecipe);
      $scope.editMode = false;
    } else {
      $location.path('/recipes');
    }
  }
  $scope.saveRecipe = function() {
    $scope.recipe.$save(function() {
      $scope.editMode = false;
      $location.path('/recipes/' + $scope.recipe.id);
    });
  };
  $scope.deleteRecipe = function() {
    $scope.recipe.$delete(function() {
      $location.path('/recipes'); //TODO: Recipe list is not reloading for some reason
    })
  }
  $scope.addInstruction = function() {
    $scope.recipe.instructions.push({ 'description': '' });
  }
}

function ShoppingListCtrl() {
  
}
