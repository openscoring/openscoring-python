from json import JSONDecoder, JSONEncoder

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

import json
import pandas
import requests
import shutil

from .metadata import __copyright__, __license__, __version__

class SimpleRequest(object):
	pass

class EvaluationRequest(SimpleRequest):

	def __init__(self, id = None, arguments = {}):
		self.id = id
		self.arguments = arguments

class SimpleResponse(object):

	def __init__(self, message = None):
		self.message = message

	def ensureSuccess(self):
		if hasattr(self, "message") and self.message is not None:
			raise Exception(self.message)
		return self

class EvaluationResponse(SimpleResponse):

	def __init__(self, message = None, id = None, result = {}):
		super(EvaluationResponse, self).__init__(message)
		self.id = id
		self.result = result

class ModelResponse(SimpleResponse):

	def __init__(self, message = None, id = None, miningFunction = None, summary = None, properties = {}, schema = {}):
		super(ModelResponse, self).__init__(message)
		self.id = id
		self.miningFunction = miningFunction
		self.summary = summary
		self.properties = properties
		self.schema = schema

class RequestEncoder(JSONEncoder):

	def default(self, request):
		if isinstance(request, SimpleRequest):
			return request.__dict__
		else:
			return JSONEncoder.default(self, request)

def _merge_dicts(user_dict, **system_dict):
	if user_dict is None:
		return system_dict
	for key in system_dict:
		system_value = system_dict[key]
		if key in user_dict:
			user_value = user_dict[key]
			if isinstance(user_value, dict) and isinstance(system_value, dict):
				user_value.update(system_value)
			elif user_value == system_value:
				pass
			else:
				raise Exception()
		else:
			user_dict[key] = system_value
	return user_dict

class Openscoring(object):

	def __init__(self, base_url = "http://localhost:8080/openscoring"):
		self.base_url = base_url

	def _model_url(self, id):
		return self.base_url + "/model/" + id

	def deployFile(self, id, file, **kwargs):
		with open(file, "rb") as instream:
			kwargs = _merge_dicts(kwargs, data = instream, json = None, headers = {"content-type" : "application/xml"})
			response = requests.put(self._model_url(id), **kwargs)
			modelResponse = ModelResponse(**json.loads(response.text))
			return modelResponse.ensureSuccess()

	def evaluate(self, id, payload = {}, **kwargs):
		if isinstance(payload, EvaluationRequest):
			evaluationRequest = payload
		else:
			evaluationRequest = EvaluationRequest(None, payload)
		kwargs = _merge_dicts(kwargs, data = json.dumps(evaluationRequest, cls = RequestEncoder), json = None, headers = {"content-type" : "application/json"})
		response = requests.post(self._model_url(id), **kwargs)
		evaluationResponse = EvaluationResponse(**json.loads(response.text))
		evaluationResponse.ensureSuccess()
		if isinstance(payload, EvaluationRequest):
			return evaluationResponse
		else:
			return evaluationResponse.result

	def evaluateCsv(self, id, df, **kwargs):
		csv = df.to_csv(None, sep = "\t", header = True, index = False, encoding = "UTF-8")
		kwargs = _merge_dicts(kwargs, data = csv, json = None, headers = {"content-type" : "text/plain"}, params = {"delimiterChar" : "\t", "quoteChar" : "\""}, stream = False)
		response = requests.post(self._model_url(id) + "/csv", **kwargs)
		try:
			if "content-encoding" in response.headers:
				response.raw.decode_content = True
			if ("content-type" in response.headers) and (response.headers["content-type"] == "application/json"):
				simpleResponse = SimpleResponse(**json.loads(response.text))
				return simpleResponse.ensureSuccess()
			return pandas.read_csv(StringIO(response.text), sep = "\t", encoding = "UTF-8")
		finally:
			response.close()

	def evaluateCsvFile(self, id, infile, outfile, **kwargs): 
		with open(infile, "rb") as instream:
			kwargs = _merge_dicts(kwargs, data = instream, json = None, headers = {"content-type" : "text/plain"}, stream = True)
			response = requests.post(self._model_url(id) + "/csv", **kwargs)
			try:
				if "content-encoding" in response.headers:
					response.raw.decode_content = True
				if ("content-type" in response.headers) and (response.headers["content-type"] == "application/json"):
					simpleResponse = SimpleResponse(**json.loads(response.text))
					return simpleResponse.ensureSuccess()
				with open(outfile, "wb") as outstream:
					shutil.copyfileobj(response.raw, outstream, 1024)
			finally:
				response.close()

	def undeploy(self, id, **kwargs):
		response = requests.delete(self._model_url(id), **kwargs)
		simpleResponse = SimpleResponse(**json.loads(response.text))
		return simpleResponse.ensureSuccess()
