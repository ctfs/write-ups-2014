page = (function() {
    page = Object.create(null);

    // class variables
    titleInterval = null;

    /**
     * Shows a beautiful login and registration page.
     */
    page.view = function view() {
        temp_main = new Template('index.html');
        temp_main.render();

        regform = document.getElementById('registerform');
        if (!!regform) {
            regform.onsubmit = form.createSubmitFunction();
        }
        loginform = document.getElementById('loginform');
        if (!!loginform) {
            loginform.onsubmit = form.createSubmitFunction(
                function _redirectToInternal() {
                    sessionStorage.setItem('loggedIn', true);
                    router.route('internal');
                }
            );
        }
    };

    return page;
})();
