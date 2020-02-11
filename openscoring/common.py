class SimpleRequest(object):
	pass

class EvaluationRequest(SimpleRequest):

	def __init__(self, id = None, arguments = {}):
		self.id = id
		self.arguments = arguments

class BatchEvaluationRequest(SimpleRequest):

	def __init__(self, id = None, requests = []):
		for request in requests:
			if not isinstance(request, EvaluationRequest):
				raise ValueError("Request element is not EvaluationRequest")
		self.id = id
		self.requests = requests

class SimpleResponse(object):

	def __init__(self, message = None):
		self.message = message

	def ensureSuccess(self):
		if hasattr(self, "message") and self.message is not None:
			raise ValueError(self.message)
		return self

class EvaluationResponse(SimpleResponse):

	def __init__(self, message = None, id = None, results = {}):
		super(EvaluationResponse, self).__init__(message)
		self.id = id
		self.results = results

class BatchEvaluationResponse(SimpleResponse):

	def __init__(self, message = None, id = None, responses = []):
		super(BatchEvaluationResponse, self).__init__(message)
		responses = [response if isinstance(response, EvaluationResponse) else EvaluationResponse(**response) for response in responses]
		self.id = id
		self.responses = responses

class ModelResponse(SimpleResponse):

	def __init__(self, message = None, id = None, miningFunction = None, summary = None, properties = {}, schema = {}):
		super(ModelResponse, self).__init__(message)
		self.id = id
		self.miningFunction = miningFunction
		self.summary = summary
		self.properties = properties
		self.schema = schema 
