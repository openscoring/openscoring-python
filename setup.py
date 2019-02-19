from distutils.core import setup

exec(open("openscoring/metadata.py").read())

setup(
	name = "openscoring",
	version = __version__,
	description = "Python client library for the Openscoring REST web service (https://github.com/openscoring/openscoring)",
	author = "Villu Ruusmann",
	author_email = "villu.ruusmann@gmail.com",
	url = "https://github.com/openscoring/openscoring-python",
	download_url = "https://github.com/openscoring/openscoring-python/archive/" + __version__ + ".tar.gz",
	license = __license__,
	classifiers = [
		"Development Status :: 5 - Production/Stable",
		"Operating System :: OS Independent",
		"Programming Language :: Python",
		"Intended Audience :: Developers",
		"Intended Audience :: Science/Research",
		"Topic :: Software Development",
		"Topic :: Scientific/Engineering"
	],
	packages = [
		"openscoring"
	],
	install_requires = [
		"pandas",
		"requests>=2.10.0"
	]
)
