loader = (function init_loader() {
    loader = Object.create(null);

    // class variables
    JS_DIR = null;
    TEMPLATE_DIR = null;

    /**
     * Initialize the JS_DIR and TEMPLATE_DIR variables.
     */
    loader.init = function init() {
        scripts = document.querySelectorAll('script');
        currentScriptSrc = scripts[scripts.length - 1].src;
        if (temp = /JS_DIR=([\/\w]+)&TEMPLATE_DIR=([\/\w]+)/.exec(currentScriptSrc)) {
            JS_DIR = temp[1];
            TEMPLATE_DIR = temp[2];
        }
    };

    /**
     * Include a JavaScript file.
     */
    loader.include = function include(path, load_cb, error_cb) {
        scriptNode = document.createElement('script');
        scriptNode.onerror = error_cb;
        scriptNode.onload = load_cb;
        scriptNode.type = 'text/javascript';
        scriptNode.src = ((!!JS_DIR) ? JS_DIR + path : path) + '.js';
        document.head.appendChild(scriptNode);
    };

    /**
     * Load a template from the TEMPLATE_DIR and cache it for further loads.
     */
    loader.loadTemplate = function loadTemplate(path) {
        content = sessionStorage.getItem('template_' + path);
        if (content == null) {
            content = http.get(TEMPLATE_DIR + path, undefined, undefined, true);
            sessionStorage.setItem('template_' + path, content);
        }
        return content;
    };

    return loader;
})();


loader.init();
