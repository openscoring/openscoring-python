from unittest import TestCase

from openscoring import Openscoring

class TestDictMerge(TestCase):

	def testMissingUserDict(self):
		self.assertEqual({}, Openscoring._merge(None))
		self.assertEqual({"A" : 1}, Openscoring._merge(None, A = 1))
		self.assertEqual({"A" : {"one" : 1}}, Openscoring._merge(None, A = {"one" : 1}))

	def testMergeValue(self):
		self.assertEqual({"A" : 1, "B" : 2, "C" : 3}, Openscoring._merge({"A" : 1}, B = 2, C = 3))

	def testMergeValueEqual(self):
		self.assertEqual({"A" : 1}, Openscoring._merge({"A" : 1}, A = 1))

	def testMergeValueConflict(self):
		with self.assertRaises(Exception):
			Openscoring._merge({"A" : 1}, A = "1")

	def testMergeDict(self):
		self.assertEqual({"A" : {"one" : 1, "two" : 2, "three" : 3}}, Openscoring._merge({"A" : {"one" : 1}}, A = {"two" : 2, "three" : 3}))

	def testMergeDictOverride(self):
		self.assertEqual({"A" : {"one" : 1}}, Openscoring._merge({"A" : {"one" : 1}}))
		self.assertEqual({"A" : {"one" : "1"}}, Openscoring._merge({"A" : {"one" : 1}}, A = {"one" : "1"}))