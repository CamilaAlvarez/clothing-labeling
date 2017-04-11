/**
 * Created by calvarez on 07-02-17.
 */

angular
    .module('Labeling')
    .controller('RegistrationCtrl', RegistrationCtrl);

RegistrationCtrl.$inject = ['$mdDialog', '$translate'];

function RegistrationCtrl($mdDialog, $translate) {
    var vm = this;
    AnonymousLoginCtrl.$inject = ['$mdDialog'];
    function AnonymousLoginCtrl($mdDialog) {
        var self = this;

        self.close = function() {
            $mdDialog.cancel();
        };
    }
    vm.showAlert = function (errorText) {
        $mdDialog.show(
            $mdDialog.alert()
                .parent(angular.element(document.querySelector('body')))
                .clickOutsideToClose(true)
                .title('Error')
                .textContent($translate.instant(errorText))
                .ariaLabel('registration error')
                .ok('Ok')
                //.targetEvent(ev)
        );
    };
    vm.showAnonymousLogin = function(){
        $mdDialog.show({
            controller: AnonymousLoginCtrl,
            controllerAs: 'ctrl',
            templateUrl: '/anonymous-user-screen/',
            parent: angular.element(document.body),
            clickOutsideToClose: true,
            fullscreen: true
        }).then(function () {

        }, function (e) {
            console.log("Closed Dialog");
        })
    }
}