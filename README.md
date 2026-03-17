# tool_template_jupyter

[![Docker Image CI](https://github.com/tool-spec/tool_template_jupyter/actions/workflows/docker-image.yml/badge.svg)](https://github.com/tool-spec/tool_template_jupyter/actions/workflows/docker-image.yml)
[![DOI](https://zenodo.org/badge/887771303.svg)](https://doi.org/10.5281/zenodo.14166903)

Template repository for building a Jupyter notebook based tool that follows the [Tool Specification](https://tool-spec.github.io/tool-specs/) container contract.

## How `gotap` works here

This template uses [`gotap`](https://github.com/tool-spec/gotap) as the default runtime shim:

```Dockerfile
CMD ["gotap", "run", "foobar", "--input-file", "/in/input.json"]
```

At build time, `gotap generate` creates `parameters.py` from `src/tool.yml`. At runtime, `run.py` uses the generated bindings, validates `/in/input.json`, and executes the notebook with [papermill](https://papermill.readthedocs.io/en/latest/).

## Required file structure

```text
/
|- in/
|  |- input.json
|- out/
|  |- ...
|- src/
|  |- tool.yml
|  |- run.py
|  |- foobar.ipynb
|  |- parameters.py   (generated at build time)
|  |- CITATION.cff
```

- `/in/input.json` contains parameter values and data references
- `/out/` receives the executed notebook and `gotap` metadata
- `/src/tool.yml` defines the tool metadata and command
- the notebook name must match the tool name from `tool.yml`

## Build and run

Build the image from the template root:

```bash
docker build -t tbr_jupyter_template .
```

Run the sample tool:

```bash
docker run --rm -it \
  -v "$(pwd)/in:/in" \
  -v "$(pwd)/out:/out" \
  -e TOOL_RUN=foobar \
  tbr_jupyter_template
```

`TOOL_RUN` is only needed when the image contains more than one tool entry. The normal execution path is still `gotap run` with `/in/input.json`.

## Customize

1. Update `src/tool.yml` to describe your tool.
2. Add notebook dependencies in `Dockerfile`.
3. Implement the notebook and wrapper logic in `src/`.
4. Rebuild the image so `gotap generate` refreshes `parameters.py`.

## Generated bindings and local notebook development

The generated `parameters.py` file is created during the image build and exposes:

- `get_parameters()`
- `get_data()`
- `get_run_context()`
- `get_logger()`

The default `docker-compose.yml` keeps the production path centered on `gotap run`. If you bind-mount `./src:/src` for notebook development, you must rebuild the image or rerun `gotap generate` inside the container so `parameters.py` stays in sync with `tool.yml`.
