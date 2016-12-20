/**
 * Created by calvarez on 15-12-16.
 */

app.factory("boundingBoxService", function(){
    var currentStatus = false;
    var getStatus = function () {
        return currentStatus;
    };
    var setStatus = function(newStatus){
        currentStatus = newStatus
    };

    return {
        getStatus: getStatus,
        setStatus: setStatus
    }
});

app.factory("boundingBoxUtils", function () {
    var Box = function (x, y, width, height) {
        this.x = x;
        this.y = y;
        this.width = width;
        this.height = height;
        this.toJson = function () {
            return {
                x: this.x,
                y: this.y,
                width : this.width,
                height: this.height
            }
        }
    };

    var createBox = function (x, y, width, height) {
        return new Box(x, y, width, height);
    };

    var checkBoundaries = function (boundingBox, boundaries) {
        var endBoundariesLeft = boundaries.x + boundaries.width;
        var endBoundariesTop = boundaries.y + boundaries.height;
        var endBBLeft = boundingBox.x + boundingBox. width;
        var endBBTop = boundingBox.y + boundingBox.height;
        var firstCondition = boundingBox.x >= boundaries.x && boundingBox.y >= boundaries.y;
        var secondCondition = boundingBox.x <= endBoundariesLeft && boundingBox.y <= endBoundariesTop;
        var thirdCondition = endBBLeft >= boundaries.x && endBBTop >= boundaries.y;
        var fourthCondition = endBBLeft <= endBoundariesLeft && endBBTop <= endBoundariesTop;
        return firstCondition && secondCondition && thirdCondition && fourthCondition;
    };

    return {
        checkBoundaries : checkBoundaries,
        createBox: createBox
    }

});