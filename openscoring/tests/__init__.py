from openscoring import _merge_dicts, EvaluationRequest, Openscoring
from pandas import DataFrame
from unittest import TestCase

import os
import pandas
import tempfile

class TestMergeDicts(TestCase):

	def testMissingUserDict(self):
		self.assertEqual({}, _merge_dicts(None))
		self.assertEqual({"A" : 1}, _merge_dicts(None, A = 1))
		self.assertEqual({"A" : {"one" : 1}}, _merge_dicts(None, A = {"one" : 1}))

	def testMergeValue(self):
		self.assertEqual({"A" : 1, "B" : 2, "C" : 3}, _merge_dicts({"A" : 1}, B = 2, C = 3))

	def testMergeValueEqual(self):
		self.assertEqual({"A" : 1}, _merge_dicts({"A" : 1}, A = 1))

	def testMergeValueConflict(self):
		with self.assertRaises(Exception):
			_merge_dicts({"A" : 1}, A = "1")

	def testMergeDict(self):
		self.assertEqual({"A" : {"one" : 1, "two" : 2, "three" : 3}}, _merge_dicts({"A" : {"one" : 1}}, A = {"two" : 2, "three" : 3}))

	def testMergeDictOverride(self):
		self.assertEqual({"A" : {"one" : 1}}, _merge_dicts({"A" : {"one" : 1}}))
		self.assertEqual({"A" : {"one" : "1"}}, _merge_dicts({"A" : {"one" : 1}}, A = {"one" : "1"}))

class TestOpenscoring(TestCase):

	def testReadme(self):
		openscoring = Openscoring()

		pmml = os.path.join(os.path.dirname(__file__), "resources", "DecisionTreeIris.pmml")

		with open(pmml, "rb") as instream:
			pmmlBytes = instream.read()
		self.assertTrue(isinstance(pmmlBytes, bytes))
		self.assertEqual(4306, len(pmmlBytes))
		modelResponse = openscoring.deploy("Iris", pmmlBytes)
		self.assertEqual("Iris", modelResponse.id)

		modelResponse = openscoring.deployFile("Iris", pmml)
		self.assertEqual("Iris", modelResponse.id)

		arguments = {
			"Sepal_Length" : 5.1,
			"Sepal_Width" : 3.5,
			"Petal_Length" : 1.4,
			"Petal_Width" : 0.2
		}
		result = openscoring.evaluate("Iris", arguments)
		self.assertEqual({"Species" : "setosa", "Probability_setosa" : 1.0, "Probability_versicolor" : 0.0, "Probability_virginica" : 0.0, "Node_Id" : "2"}, result)
		evaluationRequest = EvaluationRequest("record-001", arguments)
		evaluationResponse = openscoring.evaluate("Iris", evaluationRequest)
		self.assertEqual(evaluationRequest.id, evaluationResponse.id)
		self.assertEqual("setosa", evaluationResponse.result["Species"])

		inCsv = os.path.join(os.path.dirname(__file__), "resources", "input.csv")
		outCsv = os.path.join(tempfile.gettempdir(), "output.csv")

		df = pandas.read_csv(inCsv, sep = ",")

		result = openscoring.evaluateCsv("Iris", df)
		self.assertEqual(df["Id"].tolist(), result["Id"].tolist())
		self.assertEqual(["setosa", "versicolor", "virginica"], result["Species"].tolist())

		self.assertFalse(os.path.isfile(outCsv))
		openscoring.evaluateCsvFile("Iris", inCsv, outCsv)
		self.assertTrue(os.path.isfile(outCsv) and os.path.getsize(outCsv) > 10)

		os.remove(outCsv)

		openscoring.undeploy("Iris")

		with self.assertRaises(Exception) as context:
			openscoring.evaluate("Iris", arguments)
		self.assertEqual("Model \"Iris\" not found", str(context.exception))
