#-*- coding:utf-8 -*-

import plusplus

class TestHanja:
    def test_normal_case(self):
        src = "第一話"
        for i in xrange(1, 120):
            src = plusplus.plusone(src)
        assert src == "第百二十話"

    def test_prefix_case(self):
        src = "第一百話"
        for i in xrange(100, 111):
            src = plusplus.plusone(src)
        assert src == "第一百一十一話"

    def test_no_measure_case(self):
        src = "第一一話"
        for i in xrange(11, 100):
            src = plusplus.plusone(src)
        assert src == "第一零零話"

    def test_difficult_case(self):
        src = "第壹百話"
        for i in xrange(100, 123):
            src = plusplus.plusone(src)
        assert src == "第壹百貳拾參話"

class TestArabia:
    def test_normal_case(self):
        src = "1화"
        for i in xrange(1, 1234):
            src = plusplus.plusone(src)
        assert src == "1234화"

class TestRoma:
    def test_normal_case(self):
        src = "i"
        for i in xrange(1, 89):
            src = plusplus.plusone(src)
        assert src == "lxxxix"

    def test_normal_case(self):
        src = "I"
        for i in xrange(1, 89):
            src = plusplus.plusone(src)
        assert src == "LXXXIX"

    def test_difficult_case(self):
        #roma mode isn't work text has other latin alphabet
        items = [("I'm hero!", "I'm hero!"),
                 ("I can fly", "I can fly"),
                 ("테스트-i", "테스트-ii"),
                 ]
        for item in items:
            assert plusplus.plusone(item[0]) == item[1]

    def test_for_special(self):
        roma = [u'ⅰ', u'ⅱ', u'ⅲ', u'ⅳ', u'ⅴ', u'ⅵ', u'ⅶ', u'ⅷ', u'ⅸ', u'ⅹ']
        for i in xrange(0, 9):
            assert plusplus.plusone(roma[i]) == roma[i+1]

        roma = [u'Ⅰ', u'Ⅱ', u'Ⅲ', u'Ⅳ', u'Ⅴ', u'Ⅵ', u'Ⅶ', u'Ⅷ', u'Ⅸ', u'Ⅹ']

        for i in xrange(0, 9):
            assert plusplus.plusone(roma[i]) == roma[i+1]

