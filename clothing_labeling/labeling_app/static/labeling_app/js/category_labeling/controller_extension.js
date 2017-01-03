/**
 * Created by calvarez on 21-12-16.
 */

app.controller("CategoryLabelingController", ['$scope', '$controller', '$http', 'API', function ($scope, $controller, $http, API) {
    var canvasController = $controller("CanvasController", {$scope: $scope, this: this});
    var ctrl = this;
    var selected;
    angular.extend(this, canvasController);
    $scope.nextLabeling = function () {
        if (angular.isUndefined(ctrl.selected)){
            $window.alert("Debes elegir una categoría");
            return;
        }
        var boundingBoxJson = ctrl.buildBasicJson();
        if(angular.isUndefined(boundingBoxJson))
            return;
        boundingBoxJson.category = ctrl.selected.category;
        $scope.dataLoaded = false;
        $http.post(API.addBoundingBoxWithCategory, JSON.stringify(boundingBoxJson)).then(function (response) {
            var data = response.data;
            ctrl.changeImage(data);
            ctrl.selected = function () { return; }();
        });
    };
    $http.post(API.getCategories).then(function (response) {
        $scope.categories = response.data;
    });

    $http.post(API.nextImageCategory).then(function(response){
        var data = response.data;
        ctrl.changeImage(data);
    });
}]);