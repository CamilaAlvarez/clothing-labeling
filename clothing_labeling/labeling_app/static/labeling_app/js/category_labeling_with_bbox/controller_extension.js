/**
 * Created by calvarez on 03-01-17.
 */

app.controller("UpdateCategoryBBoxController", ['$scope', '$controller', '$http', 'API', function ($scope, $controller, $http, API) {
    var mainController = $controller("MainController", {$scope: $scope, this: this});
    var ctrl = this;
    var selected;
    angular.extend(this, mainController);
    $scope.nextLabeling = function () {
        if(angular.isUndefined(ctrl.selected)){
            $window.alert("Debes elegir una categoría");
            return;
        }
        var request = {category: ctrl.selected.category, bb_id: $scope.bb.id};
        $scope.dataLoaded = false;
        $http.post(API.updateBBoxCategory,JSON.stringify(request)).then(function (response) {
            $scope.verify = function () { return; }();
            var data = response.data;
            ctrl.loadResponse(data);
        });

    };

    $http.post(API.getCategories).then(function (response) {
        $scope.categories = response.data;
        console.log(response.data)
    });

    $http.post(API.nextBBox).then(function(response){
        var data = response.data;
        ctrl.loadResponse(data);
    });



}]);