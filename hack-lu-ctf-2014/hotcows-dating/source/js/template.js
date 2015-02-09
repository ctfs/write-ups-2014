/**
 * Template class constructor.
 */
Template = function(file) {
    this.content = loader.loadTemplate(file);
    this.vars = Object.create(null);
};

/**
 * Template class variable assignment function.
 */
Template.prototype.assign = function(value, key) {
    this.vars[key] = value;
};

/**
 * Renders the template to a string.
 */
Template.prototype.renderToString = function() {
    output = this.content;
    for (key in this.vars) {
        output = output.replace(new RegExp('{{ ' + key + ' }}', 'g'), this.vars[key]);
    }
    return output;
};

/**
 * Renders the template to the body's innerHTML. Convenience method.
 */
Template.prototype.render = function() {
    document.body.innerHTML = this.renderToString();
};
