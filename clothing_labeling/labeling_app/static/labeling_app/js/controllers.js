/**
 * Created by calvarez on 12-12-16.
 */

app.controller("CanvasController", ['$scope', '$sce', function ($scope, $sce) {

    $scope.currentImage = new Image();
    $scope.nextImage = {url: "https://pbs.twimg.com/profile_images/495099070109605888/JlDfYWTN.png" , category: "category"};
    $scope.categories = ["1","5","2","3","4"];
    //$scope.selectedType = $scope.categories[0];
    $scope.press = function () {
        console.log("hola");
    };

    $scope.currentImage.onload = function () {
        $scope.$broadcast("imageready");
    };

    $scope.sanitize = function (html) {
        $sce.getTrustedHtml(html);
    };
    $scope.currentImage.src = $scope.nextImage.url;
    $scope.element=null;

}]);

app.controller("DrawerController", ['$scope', '$compile', function ($scope, $compile) {
    var drawer = this;
    var boundingBoxId = "bounding-box";
    var withBoundingBox = false;
    var box = angular.element(document.querySelector("#" + boundingBoxId))[0];
    var mouse = {
            x: 0,
            y: 0,
            startX: 0,
            startY: 0
    };

    function setMousePosition(e) {
        var ev = e || window.event; //Moz || IE
        var titleColumn = angular.element(document.querySelector("#header-container"))[0];
        var canvasColumn = angular.element(document.querySelector("#canvas-column"))[0];
        if (ev.pageX) { //Moz
            mouse.x = ev.pageX - canvasColumn.offsetLeft;
            mouse.y = ev.pageY - titleColumn.clientHeight;
        } else if (ev.clientX) { //IE
            mouse.x = ev.clientX - canvas.offset().left//document.body.scrollLeft;
            mouse.y = ev.clientY + document.body.scrollTop;
        }
    }
    drawer.mouseDown = function($event) {
        var canvas = $event.toElement;
        if (!angular.isUndefined(box)) {
            canvas.style.cursor = "default";
            withBoundingBox = true;
        } else {
            setMousePosition($event);
            mouse.startX = mouse.x;
            mouse.startY = mouse.y;
            var element = angular.element('<div ng-mousemove="drawer.mouseMove($event)"></div>');
            box = element[0];
            box.id = boundingBoxId;
            box.className = 'rectangle';
            box.style.left = mouse.x + 'px';
            box.style.top = mouse.y + 'px';
            var canvasContainer = angular.element(document.querySelector("#canvas-container"));
            canvasContainer.append(box);
            canvas.style.cursor = "crosshair";
            $compile(box)($scope);
        }
    };
    drawer.mouseMove = function($event){
        setMousePosition($event);
        if (!angular.isUndefined(box) && !withBoundingBox) {
            box.style.width = Math.abs(mouse.x - mouse.startX) + 'px';
            box.style.height = Math.abs(mouse.y - mouse.startY) + 'px';
            box.style.left = (mouse.x - mouse.startX < 0) ? mouse.x + 'px' : mouse.startX + 'px';
            box.style.top = (mouse.y - mouse.startY < 0) ? mouse.y + 'px' : mouse.startY + 'px';
        }
    }
}]);

