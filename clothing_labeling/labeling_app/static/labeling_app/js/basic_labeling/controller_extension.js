/**
 * Created by calvarez on 21-12-16.
 */
app.controller("BasicLabelingController", ['$scope', '$controller', '$http', 'API', function ($scope, $controller,
    $http, API) {
    var canvasController = $controller("CanvasController", {$scope: $scope, this: this});
    var ctrl = this;
    angular.extend(this, canvasController);
    $scope.nextLabeling = function () {
        var boundingBoxJson = ctrl.buildBasicJson();
        if(angular.isUndefined(boundingBoxJson))
            return;
        $scope.dataLoaded = false;
        $http.post(API.addBoundingBox, JSON.stringify(boundingBoxJson)).then(function (response) {
            var data = response.data;
            ctrl.changeImage(data);
        });
    };
    $http.post(API.nextImage).then(function(response) {
        var data = response.data;
        ctrl.changeImage(data);
    });
}]);