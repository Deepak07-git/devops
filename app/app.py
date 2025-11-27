import pkgutil
import importlib.util

# Python 3.14 removed pkgutil.get_loader which some libraries (older Flask)
# still call as a fallback. Create a minimal compatibility shim so this app
# works on Python 3.14 without editing site-packages.
if not hasattr(pkgutil, "get_loader"):
    def _get_loader(name):
        try:
            spec = importlib.util.find_spec(name)
        except (ImportError, ValueError):
            return None
        if spec is None:
            return None

        loader = spec.loader

        class LoaderProxy:
            def __init__(self, spec, loader):
                self.spec = spec
                self.loader = loader
                self.origin = getattr(spec, "origin", None)

            def get_filename(self, fullname):
                if hasattr(self.loader, "get_filename"):
                    return self.loader.get_filename(fullname)
                return getattr(self.spec, "origin", None)

            @property
            def archive(self):
                return getattr(self.loader, "archive", None)

            def is_package(self, fullname):
                if hasattr(self.loader, "is_package"):
                    return self.loader.is_package(fullname)
                # spec.submodule_search_locations is set for packages
                return bool(getattr(self.spec, "submodule_search_locations", None))

        return LoaderProxy(spec, loader)

    pkgutil.get_loader = _get_loader

from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello from DevOps Flask App! Deployed using CI/CD Pipeline."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)