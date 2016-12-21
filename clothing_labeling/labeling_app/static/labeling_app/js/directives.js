/**
 * Created by calvarez on 14-12-16.
 */
app.directive("imageContainer", function(){
    function link(scope, elem){
        scope.$on("imageready", function () {
            var nextImage = scope.currentImage;
            var canvas = elem[0];
            canvas.height = nextImage.height;
            canvas.width = nextImage.width;
            var container = angular.element(document.querySelector("#canvas-container"))[0];
            container.style.width = canvas.width;
            container.style.height = canvas.height;
            var context = canvas.getContext('2d');
            context.clearRect(0,0,canvas.width,canvas.height);
            context.drawImage(scope.currentImage,0,0, canvas.width, canvas.height);
            scope.$digest();
            scope.$broadcast("imagedrawn");

        });
    }
    return{
        link: link,
        restrict: 'A'
    }
});

app.directive("sizeAware",['$window', function ($window) {

    function link(scope, elem) {
        function updateBoundingBox(){
            var canvas = angular.element(document.querySelector("canvas"))[0];
            var box = elem[0];
            box.style.left = (scope.bb.x - scope.bb.offset + canvas.offsetLeft ) + 'px';
        }
        angular.element($window).bind('resize', updateBoundingBox);
        scope.$on('destroy', function () {
           angular.element($window).off('resize', updateBoundingBox);
        });
    }
    return{
        restrict: 'A',
        link: link
    }
}]);
