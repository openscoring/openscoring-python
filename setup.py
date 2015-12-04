from distutils.core import setup

setup(
	name = "openscoring",
	version = "0.3.0",
	description = "Python client library for the Openscoring REST web service (https://github.com/jpmml/openscoring)",
	author = "Villu Ruusmann",
	author_email = "villu.ruusmann@gmail.com",
	url = "https://github.com/jpmml/openscoring-python",
	license = "GNU Affero General Public License (AGPL) version 3.0",
	packages = ["openscoring"],
	install_requires = [
		"requests"
	]
)