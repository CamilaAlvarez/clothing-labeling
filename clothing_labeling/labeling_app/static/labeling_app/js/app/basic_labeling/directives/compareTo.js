/**
 * Created by calvarez on 08-02-17.
 */

angular
    .module('Labeling')
    .directive('compareTo', compareTo);

function compareTo(){
    return{
        require:'ngModel',
        scope:{
            valueToCompare:'=compareTo'
        },
        link: function (scope, element, attrs, ngModel) {
            ngModel.$validators.compareTo = function (modelValue) {
                return modelValue == scope.valueToCompare;
            };

            scope.$watch('valueToCompare', function () {
                ngModel.$validate();
            })
        }
    }
}