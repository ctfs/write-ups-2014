page = (function() {
    page = Object.create(null);

    page.view = function view() {
        t = new Template('internal.html');
        t.render();

        btn_logout = document.getElementById('btn-logout');
        if (!!btn_logout) {
            btn_logout.onclick = function _logout() {
                router.route('logout');
            };
        }

        Array.prototype.forEach.call(
            document.querySelectorAll('.moo'),
            function _foreachMooNode(node) {
                node.onclick = function _clickMooSection() {
                    router.route('chat', node.dataset.cow);
                };
            }
        );
    };

    return page;
})();
