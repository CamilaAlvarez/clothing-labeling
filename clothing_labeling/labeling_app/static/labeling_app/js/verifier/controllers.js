/**
 * Created by calvarez on 19-12-16.
 */

var Box = function(x, y, width, height, id){
    this.x = x;
    this.y = y;
    this.width = width;
    this.height = height;
    this.id = id;
};

app.controller("MainController", ['$scope', '$http', "API", '$window',function ($scope, $http, API, $window) {
    var nextImage;
    $scope.currentImage = new Image();
    var loadResponse = function(data){
        if(angular.isDefined(data.end)){
            $scope.end = true;
            $scope.bb = undefined;
            $scope.currentImage.src = data.image.image_url;
            return;
        }
        $scope.bb = new Box(data.x, data.y, data.width, data.height, data.bb_id);
        nextImage = data.image_category.image;
        $scope.category = data.image_category.category;
        $scope.currentImage.src = nextImage.image_url;
    };
    $http.post(API.nextLabel).then(function(response){
        var data = response.data;
        loadResponse(data);
    });
    
    $scope.currentImage.onload = function () {
        $scope.$broadcast("imageready");
    };

    $scope.nextLabeling = function () {
        if(angular.isUndefined($scope.verify)){
            $window.alert("Debe elegir una opción");
            return;
        }
        var request = {correct: $scope.verify, bb_id: $scope.bb.id};
        $http.post(API.verify,JSON.stringify(request)).then(function (response) {
            var data = response.data;
            loadResponse(data);
        });

    };
}]);

app.controller("BoundingBoxController", ['$scope',"CONSTANTS", "$compile", function ($scope, CONSTANTS, $compile) {
    $scope.$watch('bb', function () {
        var rect = angular.element(document.querySelector(CONSTANTS.rectangleSelector))[0];
        var canvasContainer = angular.element(document.querySelector(CONSTANTS.canvasContainer))[0];
        if(angular.isDefined(rect)){
            rect.remove();
        }
        if(angular.isUndefined($scope.bb))
            return;
        var element = angular.element('<div></div>');
        box = element[0];
        box.className = 'rectangle';
        box.style.left = ($scope.bb.x + canvasContainer.offsetLeft) + 'px';
        box.style.top = $scope.bb.y + 'px';
        box.style.width = $scope.bb.width+'px';
        box.style.height = $scope.bb.height+'px';
        canvasContainer.append(box);
        $compile(box)($scope);

    })
}]);