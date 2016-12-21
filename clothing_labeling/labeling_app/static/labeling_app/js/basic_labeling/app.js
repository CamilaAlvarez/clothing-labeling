/**
 * Created by calvarez on 12-12-16.
 */
'use strict';
var app = angular.module("Labeling", ['ngSanitize','ui.select']);

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
    addBoundingBox: '/api/rest/write-bounding-box',
    getCategories: '/api/rest/categories',
    addBoundingBoxWithCategory: '/api/rest/write-category-bounding-box',
    nextImageCategory: '/api/rest/next-image-invalid-category'
});
