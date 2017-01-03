/**
 * Created by calvarez on 03-01-17.
 */

app.controller("VerifierController", ['$scope', '$controller', '$http', 'API', function ($scope, $controller, $http, API) {
    var mainController = $controller("MainController", {$scope: $scope, this: this});
    var ctrl = this;
    angular.extend(this, mainController);
    $scope.nextLabeling = function () {
        if(angular.isUndefined($scope.verify)){
            $window.alert("Debe elegir una opción");
            return;
        }
        var request = {correct: $scope.verify, bb_id: $scope.bb.id};
        $scope.dataLoaded = false;
        $http.post(API.verify,JSON.stringify(request)).then(function (response) {
            $scope.verify = function () { return; }();
            var data = response.data;
            ctrl.loadResponse(data);
        });

    };

    $http.post(API.nextLabel).then(function(response){
        var data = response.data;
        ctrl.loadResponse(data);
    });
    
}]);