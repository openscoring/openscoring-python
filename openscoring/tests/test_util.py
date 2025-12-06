from openscoring.util import _merge_dicts
from unittest import TestCase

class MergeDictTest(TestCase):

	def testMissingUserDict(self):
		self.assertEqual({}, _merge_dicts(None))
		self.assertEqual({"A" : 1}, _merge_dicts(None, A = 1))
		self.assertEqual({"A" : {"one" : 1}}, _merge_dicts(None, A = {"one" : 1}))

	def testMergeValue(self):
		self.assertEqual({"A" : 1, "B" : 2, "C" : 3}, _merge_dicts({"A" : 1}, B = 2, C = 3))

	def testMergeValueEqual(self):
		self.assertEqual({"A" : 1}, _merge_dicts({"A" : 1}, A = 1))

	def testMergeValueConflict(self):
		with self.assertRaises(ValueError):
			_merge_dicts({"A" : 1}, A = "1")

	def testMergeDict(self):
		self.assertEqual({"A" : {"one" : 1, "two" : 2, "three" : 3}}, _merge_dicts({"A" : {"one" : 1}}, A = {"two" : 2, "three" : 3}))

	def testMergeDictOverride(self):
		self.assertEqual({"A" : {"one" : 1}}, _merge_dicts({"A" : {"one" : 1}}))
		self.assertEqual({"A" : {"one" : "1"}}, _merge_dicts({"A" : {"one" : 1}}, A = {"one" : "1"}))
