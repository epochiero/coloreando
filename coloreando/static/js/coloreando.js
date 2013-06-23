var coloreando = angular.module('coloreando', []);


coloreando.controller('BuddiesController', function($scope) {
  $scope.buddies = [
    {username: 'example', color_id: 'red'},
  ];

});
