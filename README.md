Openscoring-Python
==================

Python client library for the Openscoring REST web service.

# Prerequisites #

* Python 2.7, 3.4 or newer.

# Installation #

Install the latest version from GitHub:
```
pip install --user --upgrade git+https://github.com/openscoring/openscoring-python.git
```

# Usage #

Creating an `Openscoring` object:
```python
from openscoring import Openscoring

os = Openscoring("http://localhost:8080/openscoring")
```

Deploying a PMML document `DecisionTreeIris.pmml` as an `Iris` model:
```python
# A dictionary of user-specified parameters
kwargs = {"auth" : ("admin", "adminadmin")}

os.deployFile("Iris", "DecisionTreeIris.pmml", **kwargs)
```

Evaluating the `Iris` model with a data record:
```python
arguments = {
	"Sepal.Length" : 5.1,
	"Sepal.Width" : 3.5,
	"Petal.Length" : 1.4,
	"Petal.Width" : 0.2
}

results = os.evaluate("Iris", arguments)
print(results)
```

The same, but wrapping the data record into an `EvaluationRequest` object for request identification purposes:
```python
from openscoring import EvaluationRequest

evaluationRequest = EvaluationRequest("record-001", arguments)

evaluationResponse = os.evaluate("Iris", evaluationRequest)
print(evaluationResponse.results)
```

Evaluating the `Iris` model with data records from the `Iris.csv` CSV file, storing the results to the `Iris-results` CSV file:
```python
os.evaluateCsvFile("Iris", "Iris.csv", "Iris-results.csv")
```

Undeploying the `Iris` model:
```python
os.undeploy("Iris", **kwargs)
```

# De-installation #

Uninstall:
```
pip uninstall openscoring
```

# License #

Openscoring-Python is dual-licensed under the [GNU Affero General Public License (AGPL) version 3.0](https://www.gnu.org/licenses/agpl-3.0.html), and a commercial license.

# Additional information #

Openscoring-Python is developed and maintained by Openscoring Ltd, Estonia.

Interested in using Openscoring software in your application? Please contact [info@openscoring.io](mailto:info@openscoring.io)
