/**
 * Created by calvarez on 08-02-17.
 */
angular
    .module('Labeling')
    .controller('LabelingCtrl', LabelingCtrl);

LabelingCtrl.$inject = ['$mdDialog', '$rootScope'];

function LabelingCtrl($mdDialog, $rootScope) {
    var self = this;
    CodesDialogCtrl.$inject = ['$mdDialog'];
    CategoryDialogCtrl.$inject = ['$scope','$mdDialog'];
    function CodesDialogCtrl( $mdDialog) {
        var vm = this;

        vm.close = function() {
            $mdDialog.cancel();
        };
    }
    function CategoryDialogCtrl($scope,$mdDialog) {
        var vm = this;
        $scope.$on('closeCategoryDialog', function () {
            $mdDialog.cancel();
        });
        vm.close = function() {
            $mdDialog.cancel();
        };
    }
    self.imageHeight = 0;
    self.imageWidth = 0;
    self.setHeight = function () {
        var canvas = document.getElementsByTagName('canvas');
        self.imageHeight = canvas[0].height;
        self.imageWidth = canvas[0].width;
    };
    self.setImage = function (image) {
        self.image = image;
    };
    self.showInstruction = function (close) {
        $mdDialog.show({
            controller: InstructionsCtrl,
            controllerAs: 'ins',
            templateUrl: '/instructions/',
            parent: angular.element(document.body),
            clickOutsideToClose: close,
            fullscreen: true
        }).then(function () {

        }, function (e) {
            console.log("Closed Dialog");
        })
    };
    self.showCodes = function(){
        $mdDialog.show({
            controller: CodesDialogCtrl,
            controllerAs: 'ctrl',
            templateUrl: '/codes/',
            parent: angular.element(document.body),
            clickOutsideToClose: true,
            fullscreen: true
        }).then(function () {

        }, function (e) {
            console.log("Closed Dialog");
        })
    };

    self.showCategoryPicture = function(image, name){
        $mdDialog.show({
            controller: CategoryDialogCtrl,
            controllerAs: 'ctrl',
            template: '<md-dialog>'+
                        '<form ng-cloak>'+
                            '<md-toolbar>'+
                                '<div class="md-toolbar-tools">'+
                                    '<h2>'+name+'</h2>'+
                                    '<span flex></span>'+
                                    '<md-button ng-click="ctrl.close()">Close</md-button>'+
                                '</div>'+
                            '</md-toolbar>'+
                        '<md-dialog-content>'+
                            '<div layout="column" layout-align="center center" layout-fill>'+
                            '<img style="max-width: 80%; max-height: 500px" src="'+image+'" />'+
                            '</div>'+
                        '</md-dialog-content>'+
                        '</form>'+
                        '</md-dialog>',
            parent: angular.element(document.body),
            clickOutsideToClose: true,
            fullscreen: true
        }).then(function () {

        }, function (e) {
            console.log("Closed Dialog");
        })
    };

}