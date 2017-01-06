/**
 * Created by calvarez on 12-12-16.
 */

app.controller("CanvasController", ['$scope', '$sce',  'boundingBoxService', 'ELEMENTS', 'boundingBoxUtils',
                                    '$window', '$http', 'API', function ($scope, $sce, boxService, ELEMENTS, boundingBoxUtils,
                                                                  $window, $http, API) {
     var ctrl = this;
     $scope.currentImage = new Image();
     $scope.dataLoaded = false;
     this.buildBasicJson = function(){
        var boundingBox = angular.element(document.querySelector(ELEMENTS.boundingBoxId))[0];
        var canvas = angular.element(document.querySelector("canvas"))[0];
        if(angular.isUndefined(boundingBox)){
            $window.alert("Debes dibujar un rectángulo");
            return;
        }
        var canvasBox = boundingBoxUtils.createBox(0, 0, canvas.width, canvas.height, 0);
        var bb = boundingBoxUtils.createBox($scope.parseDimension(boundingBox.style.left)-canvas.offsetLeft,
            $scope.parseDimension(boundingBox.style.top),
            $scope.parseDimension(boundingBox.style.width),
            $scope.parseDimension(boundingBox.style.height), canvas.offsetLeft);
        if(!boundingBoxUtils.checkBoundaries(bb, canvasBox)) {
            $window.alert("Rectángulo inválido");
            return;
        }
        var boundingBoxJson = bb.toJson();
        boundingBoxJson.image_category = ctrl.image_category;
        $scope.cleanScreen();
        return boundingBoxJson;
    };
    $scope.invalidate = function(){
        var json = {'image_category': ctrl.image_category};
        $http.post(API.invalidateImageCategory, JSON.stringify(json)).then(function(response){
            var data = response.data;
            ctrl.changeImage(data);
        });
    };
    $scope.parseDimension = function (dimension) {
        return parseInt(dimension.trim().slice(0,-2));
    };
    this.changeImage = function(data){
        $scope.nextImage = data.image;
        $scope.currentImage.src = $scope.nextImage.image_url;
        if(angular.isDefined(data.end)) {
            $scope.end = true;
            return;
        }
        $scope.category = data.category;
        ctrl.image_category = data.image_category;
    };
    $scope.currentImage.onload = function () {
        $scope.dataLoaded = true;
        $scope.$digest();
        $scope.$broadcast("imageready");
    };
    $scope.cleanScreen = function(){
        boxService.setStatus(false);
        var box = angular.element(document.querySelector(ELEMENTS.boundingBoxId))[0];
        box.remove();
    };
}]);

app.controller("DrawerController", ['$scope', '$compile', 'boundingBoxService', 'ELEMENTS', 'boundingBoxUtils',
                                    function ($scope, $compile, boxService, ELEMENTS, boundingBoxUtils) {

    var canvas = angular.element(document.querySelector("canvas"))[0];
    canvas.setAttribute("ng-mousedown", "drawer.mouseDown($event)");
    canvas.setAttribute("ng-mousemove", "drawer.mouseMove($event)");
    $compile(canvas)($scope);
    var drawer = this;
    var mouse = {
            x: 0,
            y: 0,
            startX: 0,
            startY: 0
    };

    function setMousePosition(e) {
        var ev = e || window.event; //Moz || IE
        var titleColumn = angular.element(document.querySelector(ELEMENTS.headerContainer))[0];
        var canvasColumn = angular.element(document.querySelector(ELEMENTS.canvasColumn))[0];
        if (ev.pageX) { //Moz
            mouse.x = ev.pageX - canvasColumn.offsetLeft;
            mouse.y = ev.pageY - titleColumn.clientHeight;
        } else if (ev.clientX) { //IE
            mouse.x = ev.clientX - canvasColumn.offsetLeft;
            mouse.y = ev.clientY - titleColumn.clientHeight;
        }
    }
    drawer.mouseDown = function($event) {
        var box = angular.element(document.querySelector(ELEMENTS.boundingBoxId))[0];
        if($scope.end){
            return;
        }
        var canvas = $event.toElement;
        if (angular.isDefined(box)) {
            var shape = box.style;
            $scope.bb = boundingBoxUtils.createBox($scope.parseDimension(shape.left),
                $scope.parseDimension(shape.top),
                $scope.parseDimension(shape.width),
                $scope.parseDimension(shape.height),
                canvas.offsetLeft);
            canvas.style.cursor = "default";
            boxService.setStatus(true);
        } else {
            setMousePosition($event);
            mouse.startX = mouse.x;
            mouse.startY = mouse.y;
            var element = angular.element('<div ng-mousemove="drawer.mouseMove($event)" size-aware></div>');
            box = element[0];
            box.id = ELEMENTS.boundingBoxElement;
            box.className = 'rectangle';
            box.style.left = mouse.x + 'px';
            box.style.top = mouse.y + 'px';
            var canvasContainer = angular.element(document.querySelector(ELEMENTS.canvasContainer));
            canvasContainer.append(box);
            canvas.style.cursor = "crosshair";
            $compile(box)($scope);
        }
    };
    drawer.mouseMove = function($event){
        if($scope.end)
            return;
        setMousePosition($event);
        var box = angular.element(document.querySelector(ELEMENTS.boundingBoxId))[0];
        if (angular.isDefined(box) && !boxService.getStatus()) {
            var width = Math.abs(mouse.x - mouse.startX);
            var height = Math.abs(mouse.y - mouse.startY) ;
            var left = (mouse.x - mouse.startX < 0) ? mouse.x + 'px' : mouse.startX;
            var top = (mouse.y - mouse.startY < 0) ? mouse.y + 'px' : mouse.startY;
            box.style.width = width + 'px';
            box.style.height = height + 'px';
            box.style.left = left + 'px';
            box.style.top = top + 'px';
            $scope.bb = boundingBoxUtils.createBox(left, top, width, height,canvas.offsetLeft);
        }
    }
}]);

