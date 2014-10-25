page = (function() {
    page = Object.create(null);

    /**
     * Sends an AJAX request to the logout API endpoint and redirects to the
     * index page if successful.
     */
    page.view = function view() {
        failed = function _logoutFailed() {
            showAlert('Logout failed.', true);
        };
        http.get(
            '?api=logout.php',
            function _logoutSuccess(data) {
                data = form.parseJSON(data);
                if (data['success']) {
                    sessionStorage.setItem('loggedIn', false);
                    location = '?p=index';
                } else {
                    failed();
                }
            },
            failed
        );
    };

    return page;
})();
