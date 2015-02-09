page = (function() {
    page = Object.create(null);

    /**
     * Shows the generic error template.
     */
    page.view = function view() {
        temp_main = new Template('error.html');
        temp_main.render();
    };

    return page;
})();
