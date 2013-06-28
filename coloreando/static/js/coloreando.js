var coloreando = angular.module('coloreando', []);


coloreando.controller('BuddiesController', function($scope, $http) {

  $scope.buddies = [];

  $.get('/api/getBuddies?dashboard_id=' + dashboard_id, function(data) {
    $scope.buddies = data.buddies;
    $scope.$apply();
  });

});
