/**
 * Created by calvarez on 19-12-16.
 */
var app = angular.module("Verifier",['ngSanitize','ui.select']);

app.config(['$httpProvider', function ($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);

app.constant("API", {
    nextLabel: "/api/rest/next-label",
    verify: "/api/rest/verify-label",
    nextBBox: "/api/rest/next-invalid-category-bb",
    updateBBoxCategory: "/api/rest/update-bbox-category",
    getCategories: '/api/rest/categories'
});

app.constant("CONSTANTS", {
    canvasContainer : "#canvas-container",
    rectangleSelector: ".rectangle"
});

