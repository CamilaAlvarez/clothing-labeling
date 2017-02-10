/**
 * Created by calvarez on 08-02-17.
 */
angular
    .module('Labeling')
    .controller('InstructionsCtrl', InstructionsCtrl);

InstructionsCtrl.$inject = ['$mdDialog'];

function InstructionsCtrl($mdDialog) {
    var self = this;
    self.page = 1;
    self.pages = function (numberPages) {
        self.totalPages = numberPages;
    };
    self.previousPage = function () {
        if(self.page==1)
            return;
        self.page -= 1;
    };
    self.nextPage = function () {
        if(self.page==self.totalPages)
            return;
        self.page += 1;
    };
    self.close = function(){
        $mdDialog.cancel();
    };
}