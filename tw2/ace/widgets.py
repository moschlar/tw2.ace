import tw2.core as twc
import tw2.forms as twf


ace_js = twc.JSLink(
    modname=__name__,
    filename='static/ace/ace.js',
    edit=twc.js_function('ace.edit')
    )
ace_dir = twc.DirLink(
    modname=__name__, whole_dir=True,
    filename='static/ace/',
    )

ace_min_js = twc.JSLink(
    modname=__name__,
    filename='static/ace-min/ace.js',
    edit=twc.js_function('ace.edit')
    )
ace_min_dir = twc.JSLink(
    modname=__name__, whole_dir=True,
    filename='static/ace-min/',
    )

ace_css = twc.CSSSource(src=u'''
    .ace {
        position: absolute;
        top: 0;
        right: 0;
        bottom: 0;
        left: 0;
    }
''')


class AceWidget(twf.TextArea):
    template = "genshi:tw2.ace.templates.ace"

    css_class = 'ace'
    # declare static resources here
    # you can remove either or both of these, if not needed
    resources = [ace_css, ace_js]

#    @classmethod
#    def post_define(cls):
#        pass
#        # put custom initialisation code here

    def prepare(self):
        super(AceWidget, self).prepare()
        # put code here to run just before the widget is displayed
        self.add_call(ace_js.edit(self.compound_id))
