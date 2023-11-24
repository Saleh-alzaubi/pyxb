# -*- coding: utf-8 -*-
import logging

if __name__ == '__main__':
    logging.basicConfig()
_log = logging.getLogger(__name__)
import os.path
import xml.dom.minidom as minidom
from xml.dom import Node

import pyxb.binding.generate
import pyxb.namespace
import pyxb.utils.domutils
from pyxb.utils import six

xst = '''<?xml version="1.0" encoding="utf-8"?>
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">
  <xs:simpleType name="bigpos">
    <xs:restriction base="xs:integer">
      <xs:minInclusive value="9223372036854775808"/>
      <xs:maxInclusive value="9223372036854775810"/>
    </xs:restriction>
  </xs:simpleType>
  <xs:simpleType name="bigneg">
    <xs:restriction base="xs:integer">
      <xs:minInclusive value="-9223372036854775810"/>
      <xs:maxInclusive value="-9223372036854775808"/>
    </xs:restriction>
  </xs:simpleType>
  <xs:complexType name="multiples">
    <xs:sequence>
      <xs:element name="e" minOccurs="0" maxOccurs="32" type="bigpos"/>
    </xs:sequence>
  </xs:complexType>
</xs:schema>
'''


code = pyxb.binding.generate.GeneratePython(schema_text=xst)
#open('code.py', 'w').write(code)

rv = compile(code, 'test', 'exec')
eval(rv)

import copy
import unittest

from pyxb.exceptions_ import *


class TestIssue22 (unittest.TestCase):

    SMALL = (int(1) << 63)
    LARGE = (int(1) << 63) + 2

    def testBigPos (self):
        self.assertEqual(self.SMALL, bigpos._CF_minInclusive.value())
        self.assertEqual(self.LARGE, bigpos._CF_maxInclusive.value())

    def testBigNeg (self):
        self.assertEqual(-self.SMALL, bigneg._CF_maxInclusive.value())
        self.assertEqual(-self.LARGE, bigneg._CF_minInclusive.value())

if __name__ == '__main__':
    unittest.main()
