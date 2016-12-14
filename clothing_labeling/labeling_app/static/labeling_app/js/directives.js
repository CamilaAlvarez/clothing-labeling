/**
 * Created by calvarez on 14-12-16.
 */
app.directive("imageContainer", function(){
    function link(scope, elem){
        scope.$on("imageready", function () {
            var nextImage = scope.currentImage;
            var imageHeight = nextImage.height;
            var imageWidth = nextImage.width;
            var ratio = imageHeight/imageWidth;
            var canvas = elem[0];
            canvas.height = imageHeight;
            canvas.width = imageWidth;
            var context = canvas.getContext('2d');
            context.clearRect(0,0,canvas.width,canvas.height);
            context.drawImage(scope.currentImage,0,0, canvas.width, canvas.height);

        });
    }
    return{
        link: link,
        restrict: 'A'
    }
});

/*app.directive("drawer", ['$window','$document', '$compile', function($window, $document, $compile){
    function initDraw(canvas, scope) {
        var mouse = {
            x: 0,
            y: 0,
            startX: 0,
            startY: 0
        };
        function setMousePosition(e) {
            var ev = e || window.event; //Moz || IE
            console.log(e);
            if (ev.pageX) { //Moz
                mouse.x = ev.pageX - 195;
                mouse.y = ev.pageY -69;
            } else if (ev.clientX) { //IE
                mouse.x = ev.clientX - canvas.offset().left//document.body.scrollLeft;
                mouse.y = ev.clientY + document.body.scrollTop;
            }
        }

        var element = null;
        canvas.onmousemove = function (e) {
            setMousePosition(e);
            if (element !== null) {
                element[0].style.width = Math.abs(mouse.x - mouse.startX) + 'px';
                element[0].style.height = Math.abs(mouse.y - mouse.startY) + 'px';
                element[0].style.left = (mouse.x - mouse.startX < 0) ? mouse.x + 'px' : mouse.startX + 'px';
                element[0].style.top = (mouse.y - mouse.startY < 0) ? mouse.y + 'px' : mouse.startY + 'px';
            }
        };

        canvas.onclick = function (e) {
            if (element !== null) {
                var rect = element[0].style;
                element = null;
                canvas.style.cursor = "default";
                var ctx = canvas.getContext("2d");
                ctx.beginPath();
                ctx.rect(rect.left, rect.top, rect.width, rect.height);
                ctx.fill();
                canvas.style.cursor = "default";
                console.log("finsihed.");
            } else {
                console.log("begun.");
                setMousePosition(e);
                mouse.startX = mouse.x;
                mouse.startY = mouse.y;
                element = angular.element('<div></div>');
                element[0].className = 'rectangle';
                element[0].style.left = mouse.x + 'px';
                element[0].style.top = mouse.y + 'px';
                var canvasContainer = angular.element(document.querySelector("#canvas-container"));
                console.log(canvasContainer)
                canvasContainer.append(element[0]);
                canvas.style.cursor = "crosshair";
                $compile(element[0])(scope);
                element[0].onmousemove = function (e) {
                    canvas.onmousemove(e);
                }
            }
        }
    }

    function link(scope, elem){
        initDraw(elem[0], scope)
    }
    return{
        link: link,
        restrict: 'A'
    }
}]);*/
