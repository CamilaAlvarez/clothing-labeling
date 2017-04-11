/**
 * Created by calvarez on 12-12-16.
 */
'use strict';
var app = angular.module("Labeling", ['ngMaterial','ngMessages', 'uiCropper','pascalprecht.translate']);

app.config(['$httpProvider', function ($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);

app.filter("htmlSafe", ['$sce', function($sce) {
    return function(htmlCode){
        return $sce.trustAsHtml(htmlCode);
    };
}]);

app.config(['$translateProvider', function ($translateProvider) {
    $translateProvider.registerAvailableLanguageKeys(["en","es"], {
    "en_*": "en",
    "es_*": "es"
    });
    $translateProvider.useStaticFilesLoader({
        prefix: '/static/labeling_app/js/app/language/',
        suffix: '.json'
    });
    $translateProvider.determinePreferredLanguage();
    $translateProvider.fallbackLanguage("en");
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
    nextImageCategory: '/api/rest/next-image-invalid-category',
    invalidateImageCategory: '/api/rest/invalidate-image-category'
});
