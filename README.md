Openscoring-Python
==================

Python client library for the [Openscoring REST web service] (https://github.com/jpmml/openscoring).

# Installation #

Installing the latest version from GitHub:

```
pip install --user --upgrade git+https://github.com/jpmml/openscoring-python.git
```

# Usage #

Create an `openscoring.Openscoring` object:

```python
import openscoring

os = openscoring.Openscoring("http://localhost:8080/openscoring")
```

Deploy a PMML document `DecisionTreeIris.pmml` as an `Iris` model:

```python
# A dictionary of user-specified parameters
kwargs = {"auth" : ("admin", "adminadmin")}

os.deploy("Iris", "DecisionTreeIris.pmml", **kwargs)
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

The same, but wrapping the data record into an `openscoring.EvaluationRequest` object for request identification purposes:

```python
evaluationRequest = openscoring.EvaluationRequest("record-001", arguments)
evaluationResponse = os.evaluate("Iris", evaluationRequest)
print(evaluationResponse.result)
```

Evaluate the `Iris` model with data records from the `Iris.csv` CSV file, storing the results to the `Iris-results` CSV file:

```python
os.evaluateCsv("Iris", "Iris.csv", "Iris-results.csv")
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

Openscoring-Python is dual-licensed under the [GNU Affero General Public License (AGPL) version 3.0] (http://www.gnu.org/licenses/agpl-3.0.html) and a commercial license.

# Additional information #

Please contact [info@openscoring.io] (mailto:info@openscoring.io)
