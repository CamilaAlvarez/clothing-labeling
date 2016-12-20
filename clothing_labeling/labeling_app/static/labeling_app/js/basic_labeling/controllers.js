/**
 * Created by calvarez on 12-12-16.
 */

app.controller("CanvasController", ['$scope', '$sce', '$http', 'boundingBoxService', 'ELEMENTS', 'boundingBoxUtils',
                                    'API', '$compile',function ($scope, $sce, $http, boxService, ELEMENTS, boundingBoxUtils, API, $compile) {
    var image_category;
    $scope.currentImage = new Image();
    $scope.categories = ["1","5","2","3","4"];
    $scope.element=null;
    var parseDimension = function (dimension) {
        return parseInt(dimension.trim().slice(0,-2));
    };
    var changeImage = function(data){
        $scope.nextImage = data.image;
        $scope.currentImage.src = $scope.nextImage.image_url;
        if(angular.isDefined(data.end)) {
            $scope.end = true;
            return;
        }
        $scope.category = data.category;
        image_category = data.image_category;
    };
    $scope.currentImage.onload = function () {
        $scope.$broadcast("imageready");
    };

    $scope.sanitize = function (html) {
        $sce.getTrustedHtml(html);
    };
    $scope.cleanScreen = function(){
        boxService.setStatus(false);
        var box = angular.element(document.querySelector(ELEMENTS.boundingBoxId))[0];
        box.remove();
    };
    $scope.nextLabeling = function () {
        var boundingBox = angular.element(document.querySelector(ELEMENTS.boundingBoxId))[0];
        var canvas = angular.element(document.querySelector("canvas"))[0];
        if(angular.isUndefined(boundingBox))
            return;
        var canvasContainer = angular.element(document.querySelector(ELEMENTS.canvasContainer))[0];
        var offset = canvasContainer.offsetLeft;
        var canvasBox = boundingBoxUtils.createBox(canvas.offsetLeft, 0, canvas.width, canvas.height);
        var bb = boundingBoxUtils.createBox(parseDimension(boundingBox.style.left)-offset,
            parseDimension(boundingBox.style.top),
            parseDimension(boundingBox.style.width),
            parseDimension(boundingBox.style.height));
        if(!boundingBoxUtils.checkBoundaries(bb, canvasBox))
            return;
        var boundingBoxJson = bb.toJson();
        boundingBoxJson.image_category = image_category;
        $scope.cleanScreen();
        $http.post(API.addBoundingBox, JSON.stringify(boundingBoxJson)).then(function (response) {
            var data = response.data;
            changeImage(data);
        });
    };
    $http.post(API.nextImage).then(function(response){
        var data = response.data;
        changeImage(data);
    });

}]);

app.controller("DrawerController", ['$scope', '$compile', 'boundingBoxService', 'ELEMENTS',
                                    function ($scope, $compile, boxService, ELEMENTS) {
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
            mouse.x = ev.clientX - canvas.offset().left//document.body.scrollLeft;
            mouse.y = ev.clientY + document.body.scrollTop;
        }
    }
    drawer.mouseDown = function($event) {
        var box = angular.element(document.querySelector(ELEMENTS.boundingBoxId))[0];
        if($scope.end){
            return;
        }

        var canvas = $event.toElement;
        if (!angular.isUndefined(box)) {
            canvas.style.cursor = "default";
            boxService.setStatus(true);
        } else {
            setMousePosition($event);
            mouse.startX = mouse.x;
            mouse.startY = mouse.y;
            var element = angular.element('<div ng-mousemove="drawer.mouseMove($event)"></div>');
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
        if (!angular.isUndefined(box) && !boxService.getStatus()) {
            box.style.width = Math.abs(mouse.x - mouse.startX) + 'px';
            box.style.height = Math.abs(mouse.y - mouse.startY) + 'px';
            box.style.left = (mouse.x - mouse.startX < 0) ? mouse.x + 'px' : mouse.startX + 'px';
            box.style.top = (mouse.y - mouse.startY < 0) ? mouse.y + 'px' : mouse.startY + 'px';
        }
    }
}]);

