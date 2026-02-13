# tool_template_jupyter

[![Docker Image CI](https://github.com/tool-spec/tool_template_jupyter/actions/workflows/docker-image.yml/badge.svg)](https://github.com/tool-spec/tool_template_jupyter/actions/workflows/docker-image.yml)
[![DOI](https://zenodo.org/badge/887771303.svg)](https://doi.org/10.5281/zenodo.14166903)

This is the template for a generic containerized Jupyter notebook tool following the [Tool Specification](https://tool-spec.github.io/tool-specs/) for reusable research software using Docker.

This template can be used to generate new Github repositories from it.


## How generic?

Tools using this template can be run by the [toolbox-runner](https://github.com/tool-spec/tool-runner). 
That is only convenience, the tools implemented using this template are independent of any framework.

The main idea is to implement a common file structure inside container to load inputs and outputs of the 
tool. The template shares this structures with the [Python template](https://github.com/tool-spec/tool_template_python), [R template](https://github.com/tool-spec/tool_template_r),
[NodeJS template](https://github.com/tool-spec/tool_template_node) and [Octave template](https://github.com/tool-spec/tool_template_octave), 
but can be mimiced in any container.

Each container needs at least the following structure:

```
/
|- in/
|  |- input.json
|- out/
|  |- ...
|- src/
|  |- tool.yml
|  |- run.py
|  |- toolname.ipynb
|  |- CITATION.cff
```

* `input.json` are parameters and data references.
 Whichever framework runs the container, this is how parameters are passed.
* `tool.yml` is the tool specification. It contains metadata about the scope of the tool, the number of endpoints (functions) and their parameters
* `run.py` is a Python script that handles the execution. The notebooks are executed by [papermill](https://papermill.readthedocs.io/en/latest/). 
* `toolname.ipynb` is the tool itself. The name of the notebook **must** match the name you specified in `tool.yml`. This way you can add more than one script to the container. If a single tool should run more than one notebook, you need to change the `run.py`.

## How to build the image?

You can build the image from within the root of this repo by
```
docker build -t tbr_jupyter_tempalate .
```

Use any tag you like. 

Alternatively, the contained `.github/workflows/docker-image.yml` will build the image for you 
on new releases on Github. You need to change the target repository in the aforementioned yaml.

## How to run?

This template installs the json2args python package to parse the parameters in the `/in/input.json`. This assumes that
the files are not renamed and not moved and there is actually only one tool in the container. For any other case, the environment variables
`PARAM_FILE` can be used to specify a new location for the `input.json` and `TOOL_RUN` can be used to specify the tool to be executed.
The `run.py` has to take care of that.

To invoke the docker container directly run something similar to:
```
docker run --rm -it -v /path/to/local/in:/in -v /path/to/local/out:/out -e TOOL_RUN=foobar tbr_jupyter_template
```

Then, the output will be in your local out and based on your local input folder. Stdout and Stderr are also connected to the host.

With the [toolbox runner](https://github.com/tool-spec/tool-runner), this is simplyfied:

```python
from toolbox_runner import list_tools
tools = list_tools() # dict with tool names as keys

foobar = tools.get('foobar')  # it has to be present there...
foobar.run(result_path='./', foo_int=1337, foo_string="Please change me")
```
The example above will create a temporary file structure to be mounted into the container and then create a `.tar.gz` on termination of all 
inputs, outputs, specifications and some metadata, including the image sha256 used to create the output in the current working directory.

## What about real tools, no foobar?

Yeah. 

1. change the `tool.yml` to describe your actual tool
2. add any `pip install` or `apt-get install` needed to the Dockerfile
3. add additional source code to `/src`
4. change the `toolname.ipynb` to consume parameters and data from `/in` and useful output in `out`
5. build, run, rock!

