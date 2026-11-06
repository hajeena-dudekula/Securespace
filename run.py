from importlib.util import spec_from_file_location, module_from_spec

spec = spec_from_file_location("root_app_module", "app.py")
module = module_from_spec(spec)
spec.loader.exec_module(module)

app = module.app


if __name__ == "__main__":
    app.run(debug=True)
