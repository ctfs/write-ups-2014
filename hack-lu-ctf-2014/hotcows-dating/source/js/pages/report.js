page = (function() {
    page = Object.create(null);

    page.view = function view() {
        temp_main = new Template('report.html');
        temp_main.render();

        btn_logout = document.getElementById('btn-logout');
        if (!!btn_logout) {
            btn_logout.onclick = function() {
                router.route('logout');
            };
        }
        btn_overview = document.getElementById('btn-overview');
        if (!!btn_overview) {
            btn_overview.onclick = function() {
                router.route('internal');
            };
        }
        reportform = document.getElementById('reportform');
        if (!!reportform) {
            reportform.onsubmit = form.createSubmitFunction();
        }
    };

    return page;
})();
