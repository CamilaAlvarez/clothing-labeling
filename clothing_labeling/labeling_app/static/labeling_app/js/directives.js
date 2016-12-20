/**
 * Created by calvarez on 14-12-16.
 */
app.directive("imageContainer", ['$window',function($window){
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

        });
    }
    return{
        link: link,
        restrict: 'A'
    }
}]);
