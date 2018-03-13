Openscoring-Python
==================

Python client library for the [Openscoring REST web service](https://github.com/jpmml/openscoring).

# Prerequisites #

* Python 2.7, 3.4 or newer.

# Installation #

Installing the latest version from GitHub:

```
pip install --user --upgrade git+https://github.com/jpmml/openscoring-python.git
```

# Usage #

Create an `Openscoring` object:

```python
from openscoring import Openscoring

os = Openscoring("http://localhost:8080/openscoring")
```

Deploy a PMML document `DecisionTreeIris.pmml` as an `Iris` model:

```python
# A dictionary of user-specified parameters
kwargs = {"auth" : ("admin", "adminadmin")}

os.deployFile("Iris", "DecisionTreeIris.pmml", **kwargs)
```

Evaluate the `Iris` model with a data record:

```python
arguments = {
	"Sepal_Length" : 5.1,
	"Sepal_Width" : 3.5,
	"Petal_Length" : 1.4,
	"Petal_Width" : 0.2
}

result = os.evaluate("Iris", arguments)
print(result)
```

The same, but wrapping the data record into an `EvaluationRequest` object for request identification purposes:

```python
from openscoring import EvaluationRequest

evaluationRequest = EvaluationRequest("record-001", arguments)
evaluationResponse = os.evaluate("Iris", evaluationRequest)
print(evaluationResponse.result)
```

Evaluate the `Iris` model with data records from the `Iris.csv` CSV file, storing the results to the `Iris-results` CSV file:

```python
os.evaluateCsvFile("Iris", "Iris.csv", "Iris-results.csv")
```

Undeploy the `Iris` model:

```python
os.undeploy("Iris", **kwargs)
```

# De-installation #

Uninstalling:

```
pip uninstall openscoring
```

# License #

Openscoring-Python is licensed under the [GNU Affero General Public License (AGPL) version 3.0](http://www.gnu.org/licenses/agpl-3.0.html). Other licenses are available on request.

# Additional information #

Please contact [info@openscoring.io](mailto:info@openscoring.io)
