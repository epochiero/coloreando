var coloreando = angular.module('coloreando', []);


coloreando.controller('BuddiesController', function($scope, $http) {

  $scope.buddies = [];

  $.get('http://127.0.0.1:8000/api/getBuddies?dashboard_id=' + dashboard_id, function(data) {
    $scope.buddies = data.buddies;
    $scope.$apply();
  });

  // Solicita los usuarios iniciales a la aplicacion.
  $scope.add_buddy = function(user, color) {
    $scope.buddies.push({username: user, color_id: color});
  }

});
