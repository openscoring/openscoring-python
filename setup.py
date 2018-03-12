from distutils.core import setup

from openscoring import __license__, __version__

setup(
	name = "openscoring",
	version = __version__,
	description = "Python client library for the Openscoring REST web service (https://github.com/openscoring/openscoring)",
	author = "Villu Ruusmann",
	author_email = "villu.ruusmann@gmail.com",
	url = "https://github.com/openscoring/openscoring-python",
	license = __license__,
	packages = ["openscoring"],
	install_requires = [
		"requests"
	]
)
