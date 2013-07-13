var socket = io.connect('/coloreando');
var coloreando = angular.module('coloreando', []);
coloreando.controller('BuddiesController', function($scope, $http) {

  $scope.buddies = [];

  socket.on('get_buddies_response', function(data) {
    d = JSON.parse(data);
    $scope.buddies = d.buddies;
    $scope.$apply();
  });

});
