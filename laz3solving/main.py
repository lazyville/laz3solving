def z3solve():
    print("Hello from laz3solving!")
    # Run all problem solvers, iterate each problem file and call main
    import inspect
    import pkgutil
    import importlib
    import sys
    filter_modnames = sys.argv[1:] if len(sys.argv) > 1 else []
    # Import the problems package and ensure all submodules are loaded so
    # they appear as attributes of the package module object.
    import laz3solving.problems as problems_pkg

    package_path = problems_pkg.__path__
    # Iterate all modules in the problems package and import them.
    for finder, modname, ispkg in pkgutil.iter_modules(package_path):
        if filter_modnames and modname not in filter_modnames:
            continue
        full_name = f"{problems_pkg.__name__}.{modname}"
        try:
            importlib.import_module(full_name)
        except Exception as e:
            print(f"Failed importing {full_name}: {e}")


if __name__ == "__main__":
    z3solve()
