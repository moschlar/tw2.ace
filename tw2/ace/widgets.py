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


class AceWidget(twf.TextArea):
    # declare static resources here
    # you can remove either or both of these, if not needed
    resources = [ace_js, ext_textarea_js]

    mode = twc.Param('The highlighting mode for ace', default='')

#    @classmethod
#    def post_define(cls):
#        pass
#        # put custom initialisation code here

    def prepare(self):
        super(AceWidget, self).prepare()
        # put code here to run just before the widget is displayed
        self.safe_modify('resources')
        self.add_call(ace_js.require('ace/ext/textarea').transformTextarea(twc.js_function('document.getElementById')(self.compound_id)).getSession().setMode('ace/mode/' + self.mode))
