/**
 * Created by calvarez on 12-12-16.
 */
'use strict';
var app = angular.module("Labeling", ['ngSanitize']);

app.config(['$httpProvider', function ($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);

app.constant("ELEMENTS", {
    boundingBoxId : "#bounding-box",
    boundingBoxElement: "bounding-box",
    canvasColumn : "#canvas-column",
    headerContainer : "#header-container",
    canvasContainer : "#canvas-container",
    endImage: '/media/fin.png'
});

app.constant("API",{
    nextImage: '/api/rest/next-image',
    addBoundingBox: '/api/rest/write-bounding-box'
});

//,'ui.select'