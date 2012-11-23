import os
import tw2.core as twc
import tw2.forms as twf


ace_js = twc.JSLink(
    modname=__name__,
    filename='static/ace/ace.js',
    edit=twc.js_function('ace.edit')
    )

ace_modes = dict(
    (f.strip('mode-').rstrip('.js'), twc.JSLink(modname=__name__, filename=os.path.join('static/ace', f)))
    for f in os.listdir(os.path.join(os.path.dirname(__file__), 'static/ace')) if f.startswith('mode-'))
ace_themes = dict(
    (f.strip('theme-').rstrip('.js'), twc.JSLink(modname=__name__, filename=os.path.join('static/ace', f)))
    for f in os.listdir(os.path.join(os.path.dirname(__file__), 'static/ace')) if f.startswith('theme-'))

ace_css = twc.CSSSource(src=u'''
.ace-wrapper {
    position: relative;
    width: 600px;
    height: 200px;
}
''')


class AceWidget(twf.TextArea):
    template = "tw2.ace.templates.ace"

    # declare static resources here
    # you can remove either or both of these, if not needed
    resources = [ace_js, ace_css]

#    @classmethod
#    def post_define(cls):
#        pass
#        # put custom initialisation code here

    def prepare(self):
        super(AceWidget, self).prepare()
        # put code here to run just before the widget is displayed
        self.add_call(ace_js.edit(self.compound_id).getSession().setMode('ace/mode/java'))
