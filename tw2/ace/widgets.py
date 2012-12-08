import os
import tw2.core as twc
import tw2.forms as twf


ace_js = twc.JSLink(
    modname=__name__,
    filename='static/ace/ace.js',
    edit=twc.js_function('ace.edit'),
    require=twc.js_function('ace.require'),
    )
ext_textarea_js = twc.JSLink(
    modname=__name__,
    filename='static/ace/ext-textarea.js',
    #Not safe for multiple widget instances per request
    #transformTextarea=ace_js.require('ace/ext/textarea').transformTextarea
    )

ace_modes = dict(
    (f.strip('mode-').rstrip('.js'), twc.JSLink(modname=__name__, filename=os.path.join('static/ace', f)))
    for f in os.listdir(os.path.join(os.path.dirname(__file__), 'static/ace')) if f.startswith('mode-'))
ace_themes = dict(
    (f.strip('theme-').rstrip('.js'), twc.JSLink(modname=__name__, filename=os.path.join('static/ace', f)))
    for f in os.listdir(os.path.join(os.path.dirname(__file__), 'static/ace')) if f.startswith('theme-'))


init_js = twc.JSSource(src=u'''
// Globals
var ace_textarea = ace.require("ace/ext/textarea");
var ace_editors = {};

function tw2_ace(target, theme, mode, options) {
    var editor = ace_textarea.transformTextarea(document.getElementById(target));
    var session = editor.getSession();

    if (theme) {
        editor.setTheme("ace/theme/" + theme);
    };
    if (mode) {
        session.setMode("ace/mode/" + mode);
    };

    if (options) {
        editor.renderer.setShowGutter(options.show_gutter);
        if (Boolean(options.soft_wrap)) {
            session.setUseWrapMode(true);
            var col = parseInt(options.soft_wrap, 10);
            if (isNaN(col))
                col = null;
            session.setWrapLimitRange(col, col);
        } else {
            session.setUseWrapMode(false);
        }
    }

    var p = document.createElement("pre");
    p.style.visibility = "hidden";
    p = document.body.appendChild(p);
    var s = window.getComputedStyle(p);
    editor.container.style.fontSize = s.fontSize;
    editor.container.style.fontFamily = s.fontFamily;

    ace_editors[target] = editor;
    return editor;
}
''', tw2_ace=twc.js_function('tw2_ace'))


def mode_name(mode):
    '''Tries best-effortly to get the right mode name'''

    if mode:
        l = mode.lower()

        if l in ('c', 'c++', 'cxx'):
            return 'c_cpp'

        if l in ('bash', ):
            return 'sh'

        if l in ace_modes:
            return l

    return None


class AceWidget(twf.TextArea):
    # declare static resources here
    # you can remove either or both of these, if not needed
    resources = [ace_js, ext_textarea_js, init_js]

    mode = twc.Param('The highlighting mode for ace', default='')

    show_gutter = twc.Param(default=True)
    soft_wrap = twc.Param(u'''Possible values:
False:
    No soft wrap
True:
    Free soft wrap on editor border
Integer:
    Soft wrap after specified characters
''', default=True)

#    @classmethod
#    def post_define(cls):
#        pass
#        # put custom initialisation code here

    def prepare(self):
        super(AceWidget, self).prepare()
        # put code here to run just before the widget is displayed
        self.safe_modify('resources')
        mode = mode_name(self.mode)
        options = dict(
            show_gutter=self.show_gutter,
            soft_wrap=self.soft_wrap
            )
        self.add_call(init_js.tw2_ace(self.compound_id, None, mode, options))
