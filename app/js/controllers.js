'use strict';

/* Controllers */


function HomeCtrl() {
  
}

function NavbarCtrl($scope, User) {
  $scope.user = User.get(); //TODO: What if user is not logged in?
}

function UserDetailCtrl($scope, User) {
  //TODO: Loading
  $scope.user = User.get(); //TODO: What if user is not logged in?
  $scope.saveUser = function() {
    //TODO: Loading
    $scope.user.$save();
  }
}

function RecipeListCtrl($scope, Recipe) {
  $scope.recipes = Recipe.query();
}

function RecipeDetailCtrl($scope, Recipe, $routeParams, $location) {
  //TODO: Loading...
  if ($routeParams.recipeId.toLowerCase() == 'new') {
    $scope.recipe = new Recipe();
    $scope.recipe.instructions = [];
    $scope.recipe.ingredients = [];
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
  };
  $scope.saveRecipe = function() {
    //TODO: Loading...
    $scope.recipe.$save(function() {
      $scope.editMode = false;
      $location.path('/recipes/' + $scope.recipe.id);
    });
  };
  $scope.deleteRecipe = function() {
    //TODO: Loading...
    $scope.recipe.$delete(function() {
      $location.path('/recipes'); //TODO: Recipe list is not reloading for some reason
    })
  };
  $scope.addInstruction = function() {
    $scope.recipe.instructions.push({}); //TODO: Set focus to just-added instruction
  };
  $scope.addIngredient = function() {
    $scope.recipe.ingredients.push({}); //TODO: Set focus to just-added ingredient
  }
}

function ShoppingListCtrl() {
  
}
