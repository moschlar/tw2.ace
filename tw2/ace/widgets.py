import tw2.core as twc


class Ace(twc.Widget):
    template = "genshi:tw2.ace.templates.ace"

    # declare static resources here
    # you can remove either or both of these, if not needed
    resources = [
        twc.JSLink(modname=__name__, filename='static/ace.js'),
        twc.CSSLink(modname=__name__, filename='static/ace.css'),
    ]

    @classmethod
    def post_define(cls):
        pass
        # put custom initialisation code here

    def prepare(self):
        super(Ace, self).prepare()
        # put code here to run just before the widget is displayed
