# -*- coding: utf-8 -*-

################################################################
# xmldirector.twitter
# (C) 2016,  Andreas Jung, www.zopyx.com, Tuebingen, Germany
################################################################


from unittest import TestCase

from xmldirector.twitter.browser.rewriterules import RuleRewriter


rules = [
    ('src/word/(.*).docx', 'out/$1.docx'),
    ('src/(.*)', '$1'),
    ('xxx/(.*)', 'hello/world/$1'),
]

invalid_rules = [
    ('((((.*).docx', 'out/$1.docx'),
]


class RuleRewriterTests(TestCase):

    def test_rewrite(self):
        rewriter = RuleRewriter(rules)
        rw = rewriter.rewrite
        self.assertEqual(rw('src/word/index.docx'), 'out/index.docx')
        self.assertEqual(rw('src/word/sample.docx'), 'out/sample.docx')
        self.assertEqual(rw('src/hello/world/hello.png'), 'hello/world/hello.png')
        self.assertEqual(rw('xxx/dummy'), 'hello/world/dummy')
        self.assertEqual(rw('nix'), None)

    def test_invalid_rules(self):

        with self.assertRaises(ValueError):
            rewriter = RuleRewriter(invalid_rules)
