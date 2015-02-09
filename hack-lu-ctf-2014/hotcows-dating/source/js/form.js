/**
 * Show an alert box without using alert() BECAUSE ITS UGLY AND SHIT.
 */
function showAlert(message, is_error) {
    currentAlert = document.createElement('div');
    className = (is_error) ? 'alert-error' : 'alert-message';
    currentAlert.setAttribute('class', 'alert ' + className);
    currentMessage = document.createElement('p');
    currentMessage.appendChild(document.createTextNode(message));
    currentAlert.appendChild(currentMessage);
    button = document.createElement('button');
    button.appendChild(document.createTextNode('close'));
    button.onclick = function _closeAlert() {
        document.body.removeChild(currentAlert);
    };
    currentMessage.appendChild(button);
    document.body.appendChild(currentAlert);
};


form = (function() {
    form = Object.create(null);

    /**
     * Serialize form data.
     */
    form.serialize = function serialize(form_node) {
        query = [];
        for (i = 0; i < form_node.length; i++) {
            if (form_node[i].hasAttribute('name')) {
                query.push(encodeURIComponent(form_node[i].getAttribute('name')) + '=' + encodeURIComponent(form_node[i].value));
            }
        }
        return query.join('&');
    };

    /**
     * Parse the backend's JSON with security prefix.
     */
    form.parseJSON = function parseJSON(data) {
        return JSON.parse(data.slice(5));
    };

    /**
     * Returns a function which can be used for the onsubmit event of forms.
     */
    form.createSubmitFunction = function createSubmitFunction(success_cb, failure_cb) {
        return function submitForm(e) {
            e.preventDefault();

            standard_cb = function standardFormCallback(data) {
                showAlert(data['message'], !data['success']);
            };
            success_cb = success_cb || standard_cb;
            failure_cb = failure_cb || standard_cb;

            http.post(
                '?api=' + e.target.getAttribute('action'),
                form.serialize(e.target),
                function _httpLoad(content) {
                    data = form.parseJSON(content);
                    if (data['success']) {
                        success_cb(data);
                    } else {
                        failure_cb(data);
                    }
                },
                function _httpError() {
                    showAlert('Unknown network error.', true);
                }
            );
            e.target.reset();
        };
    };

    return form;
})();
