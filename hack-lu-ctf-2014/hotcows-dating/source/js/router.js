router = (function _routerClosure() {
    router = Object.create(null);

    /**
     * Routes to the page in the URL when the page is loaded.
     */
    router.init = function init() {
        router.route((m = /p=(\w+)/.exec(temp=location)) ? m[1] : 'index',
                     (!!temp.hash) ? temp.hash.slice(1) : undefined);
    };

    /**
     * Checks if the logged-in state allows access to the current site and sets
     * the URL accordingly. Finally, router.show is called.
     */
    router.route = function route(page_name, args) {
        loggedIn = sessionStorage.getItem('loggedIn');
        if (loggedIn == 'true') {
            if (page_name == 'index') {
                page_name = 'internal';
            }
        } else {
            page_name = 'index';
        }
        args = (!!args) ? '#' + args : '';
        history.pushState({}, page_name, '?p=' + page_name + args);
        router.show(page_name, args);
    };

    /**
     * Loads a script from the JS_DIR/pages/ directory and calls the page.view()
     * function.
     */
    router.show = function show(page_name) {
        success = function _success() { page.view() };
        failure = function failure() {
            if (page_name != 'error') {
                router.show('error');
            } else {
                // well, fuck
                document.write("<h1>Something went wrong.</h1>" +
                               "<h2>Don't ask us.</h2>" +
                               "<h3>We're probably not responsible.</h3>" +
                               "<h4>Go away.</h4>");
            }
        };

        // optional destructor
        if (window.page && window.page.destroy) {
            page.destroy();
        }

        // load page
        loader.include('pages/' + page_name, success, failure);
    };


    scripts = document.querySelectorAll('script');
    currentScriptSrc = scripts[scripts.length - 1].src;
    if (currentScriptSrc[currentScriptSrc.length - 1] == '1') {
        sessionStorage.setItem('loggedIn', true);
    }

    return router;
})();


onload = router.init;
onpopstate = router.init;
