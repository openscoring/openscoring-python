from openscoring import _merge_dicts, BatchEvaluationRequest, EvaluationRequest, Openscoring
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
		self.assertEqual(2919, len(pmmlBytes))
		modelResponse = openscoring.deploy("Iris", pmmlBytes)
		self.assertEqual("Iris", modelResponse.id)

		modelResponse = openscoring.deployFile("Iris", pmml)
		self.assertEqual("Iris", modelResponse.id)

		arguments = {
			"Sepal.Length" : 5.1,
			"Sepal.Width" : 3.5,
			"Petal.Length" : 1.4,
			"Petal.Width" : 0.2
		}
		result = openscoring.evaluate("Iris", arguments)
		self.assertEqual({"Species" : "setosa", "probability(setosa)" : 1.0, "probability(versicolor)" : 0.0, "probability(virginica)" : 0.0}, result)
		evaluationRequest = EvaluationRequest("record-001", arguments)
		evaluationResponse = openscoring.evaluate("Iris", evaluationRequest)
		self.assertEqual(evaluationRequest.id, evaluationResponse.id)
		self.assertEqual("setosa", evaluationResponse.result["Species"])

		batchArguments = [
			{
				"Petal.Length" : 1.4,
				"Petal.Width" : 0.2
			},
			{
				"Petal.Length" : 4.7,
				"Petal.Width" : 1.4
			},
			{
				"Petal.Length" : 3.6,
				"Petal.Width" : 2.5
			}
		]
		result = openscoring.evaluateBatch("Iris", batchArguments)
		self.assertEquals(3, len(result))
		self.assertEquals({"Species" : "setosa", "probability(setosa)" : 1.0, "probability(versicolor)" : 0.0, "probability(virginica)" : 0.0}, result[0])
		self.assertEquals({"Species" : "versicolor", "probability(setosa)" : 0.0, "probability(versicolor)" : (49.0 / 54.0), "probability(virginica)" : (5.0 / 54.0)}, result[1])
		self.assertEquals({"Species" : "virginica", "probability(setosa)" : 0.0, "probability(versicolor)" : (1.0 / 46.0), "probability(virginica)" : (45.0 / 46.0)}, result[2])
		evaluationRequests = [EvaluationRequest(None, arguments) for arguments in batchArguments]
		batchEvaluationRequest = BatchEvaluationRequest("batch-A", evaluationRequests)
		batchEvaluationResponse = openscoring.evaluateBatch("Iris", batchEvaluationRequest)
		self.assertEqual(batchEvaluationRequest.id, batchEvaluationResponse.id)
		evaluationResponses = batchEvaluationResponse.responses
		self.assertEqual(3, len(evaluationResponses))
		self.assertEqual("setosa", evaluationResponses[0].result["Species"])
		self.assertEqual("versicolor", evaluationResponses[1].result["Species"])
		self.assertEqual("virginica", evaluationResponses[2].result["Species"])

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
