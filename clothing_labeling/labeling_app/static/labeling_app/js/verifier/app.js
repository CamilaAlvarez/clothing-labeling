/**
 * Created by calvarez on 19-12-16.
 */
var app = angular.module("Verifier",[]);

app.config(['$httpProvider', function ($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);

app.constant("API", {
    nextLabel: "/api/rest/next-label",
    verify: "/api/rest/verify-label"
});

app.constant("CONSTANTS", {
    canvasContainer : "#canvas-container",
    rectangleSelector: ".rectangle"
});

