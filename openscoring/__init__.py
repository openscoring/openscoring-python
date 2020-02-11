from requests.auth import AuthBase
from json import JSONDecoder, JSONEncoder

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

import json
import pandas
import requests
import shutil

from .common import *
from .metadata import __copyright__, __license__, __version__

class RequestEncoder(JSONEncoder):

	def default(self, request):
		if isinstance(request, SimpleRequest):
			return request.__dict__
		else:
			return JSONEncoder.default(self, request)

class BearerTokenAuth(AuthBase):

	def __init__(self, token):
		self.token = token

	def __call__(self, request):
		request.headers["authorization"] = "Bearer {}".format(self.token)
		return request

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
				raise ValueError("Key {} has differing values {} and {}".format(key, user_value, system_value))
		else:
			user_dict[key] = system_value
	return user_dict

class Openscoring(object):

	def __init__(self, base_url, token = None):
		self.base_url = base_url
		self.auth = None
		if token is not None:
			self.auth = BearerTokenAuth(token)

	def _model_url(self, id):
		return "{}/model/{}".format(self.base_url, id)

	def _check_response(self, response):
		try:
			service = response.headers["X-Application"]
			if service.startswith("Openscoring/2.0") is False:
				raise ValueError(service)
		except (KeyError, ValueError) as e:
			raise ValueError("The web server at {} did not identify itself as Openscoring/2.0 service".format(self.base_url))
		return response

	def deploy(self, id, pmml, **kwargs):
		kwargs = _merge_dicts(kwargs, data = pmml, json = None, auth = self.auth, headers = {"content-type" : "application/xml"})
		response = self._check_response(requests.put(self._model_url(id), **kwargs))
		modelResponse = ModelResponse(**json.loads(response.text))
		return modelResponse.ensureSuccess()

	def deployFile(self, id, file, **kwargs):
		with open(file, "rb") as instream:
			return self.deploy(id, instream, **kwargs)

	def evaluate(self, id, payload = {}, **kwargs):
		if isinstance(payload, EvaluationRequest):
			evaluationRequest = payload
		else:
			evaluationRequest = EvaluationRequest(None, payload)
		kwargs = _merge_dicts(kwargs, data = json.dumps(evaluationRequest, cls = RequestEncoder), json = None, auth = self.auth, headers = {"content-type" : "application/json"})
		response = self._check_response(requests.post(self._model_url(id), **kwargs))
		evaluationResponse = EvaluationResponse(**json.loads(response.text))
		evaluationResponse.ensureSuccess()
		if isinstance(payload, EvaluationRequest):
			return evaluationResponse
		else:
			return evaluationResponse.results

	def evaluateBatch(self, id, payload = [], **kwargs):
		if isinstance(payload, BatchEvaluationRequest):
			batchEvaluationRequest = payload
		else:
			evaluationRequests = [EvaluationRequest(None, arguments) for arguments in payload]
			batchEvaluationRequest = BatchEvaluationRequest(None, evaluationRequests)
		kwargs = _merge_dicts(kwargs, data = json.dumps(batchEvaluationRequest, cls = RequestEncoder), json = None, auth = self.auth, headers = {"content-type" : "application/json"})
		response = self._check_response(requests.post(self._model_url(id) + "/batch", **kwargs))
		batchEvaluationResponse = BatchEvaluationResponse(**json.loads(response.text))
		batchEvaluationResponse.ensureSuccess()
		if isinstance(payload, BatchEvaluationRequest):
			return batchEvaluationResponse
		else:
			evaluationResponses = batchEvaluationResponse.responses
			return [evaluationResponse.results for evaluationResponse in evaluationResponses]

	def evaluateCsv(self, id, df, **kwargs):
		csv = df.to_csv(None, sep = "\t", header = True, index = False, encoding = "UTF-8")
		kwargs = _merge_dicts(kwargs, data = csv, json = None, auth = self.auth, headers = {"content-type" : "text/plain"}, params = {"delimiterChar" : "\t", "quoteChar" : "\""}, stream = False)
		response = self._check_response(requests.post(self._model_url(id) + "/csv", **kwargs))
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
			kwargs = _merge_dicts(kwargs, data = instream, json = None, auth = self.auth, headers = {"content-type" : "text/plain"}, stream = True)
			response = self._check_response(requests.post(self._model_url(id) + "/csv", **kwargs))
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
		kwargs = _merge_dicts(kwargs, auth = self.auth)
		response = self._check_response(requests.delete(self._model_url(id), **kwargs))
		simpleResponse = SimpleResponse(**json.loads(response.text))
		return simpleResponse.ensureSuccess()
