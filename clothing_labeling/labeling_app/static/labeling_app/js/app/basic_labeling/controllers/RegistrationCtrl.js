/**
 * Created by calvarez on 07-02-17.
 */

angular
    .module('Labeling')
    .controller('RegistrationCtrl', RegistrationCtrl);

RegistrationCtrl.$inject = ['$mdDialog'];

function RegistrationCtrl($mdDialog) {
    var vm = this;
    vm.showAlert = function (errorText) {
        $mdDialog.show(
            $mdDialog.alert()
                .parent(angular.element(document.querySelector('body')))
                .clickOutsideToClose(true)
                .title('Error')
                .textContent(errorText)
                .ariaLabel('registration error')
                .ok('Ok')
                //.targetEvent(ev)
        );
    }
}