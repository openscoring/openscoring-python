#!/usr/bin/env python

from json import JSONDecoder, JSONEncoder

import json
import requests

__copyright__ = "Copyright (c) 2015 Villu Ruusmann"
__license__ = "GNU Affero General Public License (AGPL) version 3.0"

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
		if(hasattr(self, "message") and self.message is not None):
			raise Exception(self.message)
		return self

class EvaluationResponse(SimpleResponse):

	def __init__(self, message = None, id = None, result = {}):
		SimpleResponse.__init__(self, message)
		self.id = id
		self.result = result

class ModelResponse(SimpleResponse):

	def __init__(self, message = None, id = None, miningFunction = None, summary = None, properties = {}, schema = {}):
		SimpleResponse.__init__(self, message)
		self.id = id
		self.miningFunction = miningFunction
		self.summary = summary
		self.properties = properties
		self.schema = schema

class RequestEncoder(JSONEncoder):

	def default(self, request):
		if(isinstance(request, SimpleRequest)):
			return request.__dict__
		else:
			return JSONEncoder.default(self, request)

class Openscoring:

	def __init__(self, baseUrl = "http://localhost:8080/openscoring", auth = None):
		self.baseUrl = baseUrl
		self.auth = auth

	def deploy(self, id, pmml):
		stream = open(pmml, "rb")
		try :
			response = requests.put(self.baseUrl + "/model/" + id, auth = self.auth, headers = {"content-type" : "application/xml"}, data = stream)
			modelResponse = ModelResponse(**json.loads(response.content))
			return modelResponse.ensureSuccess()
		finally:
			stream.close()

	def evaluate(self, id, payload = {}):
		if(isinstance(payload, EvaluationRequest)):
			evaluationRequest = payload
		else:
			evaluationRequest = EvaluationRequest(None, payload)
		response = requests.post(self.baseUrl + "/model/" + id, auth = self.auth, headers = {"content-type" : "application/json"}, data = json.dumps(evaluationRequest, cls = RequestEncoder))
		evaluationResponse = EvaluationResponse(**json.loads(response.content))
		evaluationResponse.ensureSuccess()
		if(isinstance(payload, EvaluationRequest)):
			return evaluationResponse
		else:
			return evaluationResponse.result

	def undeploy(self, id):
		response = requests.delete(self.baseUrl + "/model/" + id, auth = self.auth)
		simpleResponse = SimpleResponse(**json.loads(response.content))
		return simpleResponse.ensureSuccess()