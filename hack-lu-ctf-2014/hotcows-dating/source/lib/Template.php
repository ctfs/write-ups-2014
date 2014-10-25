<?php
if (!defined('MAIN')) exit();


/**
 * Generic Template class.
 *
 * Includes the templates, so PHP Code in templates is possible, but should be
 * reduced to a minimum.
 *
 * Example of usage:
 * $t = new Template('templates/template.php');
 * $t->assign('key', 'value');
 * $t->render(array('another_key' => 'value'));
 *
 * That's it, folks!
 *
 * @author qll
 */
class Template {
    protected $template;
    protected $pvars;   // holds persistent variables for all Templates
    protected $vars;    // holds variables for this Template
    protected $blocks;  // holds blocks defined in child templates
    protected $parent;  // parent Template
    protected $current_block;

    /**
     * Takes the template include path as an argument.
     * The second argument is an array with permanent variables that should be
     * available in all templates (parent, children).
     */
    public function __construct($template, array $pvars=array()) {
        $this->template = $template;
        $this->vars = array();
        $this->pvars = $pvars;
        $this->blocks = array();
        $this->current_block = '';
    }

    /**
     * Gets previously assigned Template variable.
     */
    protected function get($key, $default=null) {
        if (!isset($this->vars[$key])) {
            if (!is_null($default)) {
                return $default;
            }
            throw new TemplateException('Undefined key: ' . $key);
        }
        if (empty($this->vars[$key]) && !is_null($default)) {
            return $default;
        }
        return $this->vars[$key];
    }

    /**
     * Assigns a variable $key to a $value to use it in the template.
     */
    public function assign($value, $key) {
        $this->vars[$key] = $value;
    }

    /**
     * Assigns a block to a Template. Blocks can be filled by child Templates.
     */
    public function assign_block($content, $key) {
        $this->blocks[$key] = $content;
    }

    /**
     * Renders template to output.
     * $vars contains additional template variables.
     */
    public function render(array $vars=array()) {
        foreach ($vars as $key => $value) {
            $this->assign($key, $value);
        }
        include $this->template;
        if (!empty($this->parent)) {
            foreach ($this->pvars as $key => $value) {
                $this->parent->assign($key, $value);
            }
            $this->parent->render();
        }
    }

    /**
     * Takes a path to another template and makes that the parent of the
     * current template.
     */
    protected function extend($template) {
        $this->parent = new Template($template, $this->pvars);
    }

    /**
     * Defines a block for the parent template. MUST be followed by
     * $this->end_block($name);.
     *
     * Example:
     * <?php $this->extend('main.html'); ?>
     * <?php $this->start_block('content'); ?>
     *   <div id="something">
     *     Some content
     *   </div>
     * <?php $this->end_block('content'); ?>
     *
     * The variable content will be available in the parent template now.
     * Parent can do <?php echo $this->block('content'); ?>
     */
    protected function start_block($name) {
        if (empty($this->parent)) {
            throw new TemplateException('Parent needs to be defined with '
                                        . '$this->extend($t) before ' . $name
                                        . ' can be started.'
            );
        }
        $this->current_block = $name;
        ob_start();
    }

    /**
     * Stops the definition of a block. Name is optional.
     */
    protected function end_block($name=null) {
        if (empty($this->current_block)) {
            throw new TemplateException('No block was opened.');
        }
        if (!is_null($name) && $name != $this->current_block) {
            throw new TemplateException("Closing a block that wasn't open in "
                                        . "the first place (" . $name
                                        . " closed, but " . $this->current_block
                                        . " was open).");
        }
        $content = ob_get_contents();
        ob_end_clean();
        $this->parent->assign_block($this->current_block, $content);
        $this->current_block = '';
    }

    /**
     * Returns a block with the Name $key. If it does not exist return an empty
     * string.
     */
    protected function block($key) {
        return (isset($this->blocks[$key])) ? $this->blocks[$key] : '';
    }
}


class TemplateException extends Exception {}
