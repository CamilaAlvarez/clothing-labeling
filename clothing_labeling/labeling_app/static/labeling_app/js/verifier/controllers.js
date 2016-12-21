/**
 * Created by calvarez on 19-12-16.
 */

var Box = function(x, y, width, height, id, offset){
    this.x = x;
    this.y = y;
    this.width = width;
    this.height = height;
    this.id = id;
    this.offset = offset;
};

app.controller("MainController", ['$scope', '$http', "API", '$window',function ($scope, $http, API, $window) {
    var nextImage;
    $scope.currentImage = new Image();
    var loadResponse = function(data){
        if(angular.isDefined(data.end)){
            $scope.end = true;
            $scope.bb = function () { return; }();;
            $scope.currentImage.src = data.image.image_url;
            return;
        }
        var canvas = angular.element(document.querySelector("canvas"))[0];
        $scope.bb = new Box(data.x, data.y, data.width, data.height, data.bb_id, 0);
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
            $scope.verify = function () { return; }();
            var data = response.data;
            loadResponse(data);
        });

    };
}]);

app.controller("BoundingBoxController", ['$scope',"CONSTANTS", "$compile", '$window', function ($scope, CONSTANTS, $compile, $window) {
    function updateRect() {
        var rect = angular.element(document.querySelector(CONSTANTS.rectangleSelector))[0];
        var canvasContainer = angular.element(document.querySelector(CONSTANTS.canvasContainer))[0];
        var canvas = angular.element(document.querySelector("canvas"))[0];
        if(angular.isDefined(rect)){
            rect.remove();
        }
        if(angular.isUndefined($scope.bb))
            return;
        var element = angular.element('<div size-aware></div>');
        box = element[0];
        box.className = 'rectangle';
        box.style.left = ($scope.bb.x + canvas.offsetLeft ) + 'px';
        box.style.top = $scope.bb.y + 'px';
        box.style.width = $scope.bb.width+'px';
        box.style.height = $scope.bb.height+'px';
        canvasContainer.append(box);
        box.style.left = ($scope.bb.x + canvas.offsetLeft ) + 'px';

        $compile(box)($scope);
        canvas = angular.element(document.querySelector("canvas"))[0];
    }
    $scope.$on('imagedrawn', function () {
        updateRect()
    });
}]);