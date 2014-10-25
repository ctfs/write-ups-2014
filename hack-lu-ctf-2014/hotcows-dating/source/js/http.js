http = (function _httpClosure() {
    http = Object.create(null);

    /**
     * Generic XMLHttpRequest function. Capable of synchronous and asynchronous
     * data loading. Asynchronous data is returned via callbacks, synchronous
     * loaded data is directly returned.
     */
    sendXhr = function(uri, method, data, load_cb, error_cb, synchronous) {
        x = new XMLHttpRequest();
        x.onload = function() { if (load_cb) load_cb(x.responseText); };
        x.onerror = error_cb;
        x.open(method, uri, !synchronous);
        if (method == 'POST') {
            x.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
        }
        x.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
        x.send(data);
        if (synchronous) {
            return x.responseText;
        }
    };

    /**
     * For simplicity.
     */
    http.get = function get(uri, load_cb, error_cb, synchronous) {
        return sendXhr(uri, 'GET', '', load_cb, error_cb, synchronous);
    };

    /**
     * For simplicity.
     */
    http.post = function post(uri, data, load_cb, error_cb, synchronous) {
        return sendXhr(uri, 'POST', data, load_cb, error_cb, synchronous);
    }

    return http;
})();
