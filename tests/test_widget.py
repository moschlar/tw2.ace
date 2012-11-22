from tw2.core.testbase import WidgetTest
from tw2.ace import *

class TestAce(WidgetTest):
    # place your widget at the TestWidget attribute
    widget = Ace
    # Initilization args. go here 
    attrs = {'id':'ace-test'}
    params = {}
    expected = """<div id="ace-test"></div>"""
