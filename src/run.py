import logging
import os
import sys
from pathlib import Path

import papermill as pm

from parameters import get_data, get_logger, get_parameters

params = get_parameters()
data = get_data()
structured_logger = get_logger()

toolname = os.environ.get("TOOL_RUN", "foobar").lower()
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

structured_logger.info("start", "Starting notebook tool run", tool=toolname)
structured_logger.info(
    "input-loaded",
    "Loaded validated parameters and data paths",
    tool=toolname,
    parameter_count=len(vars(params)),
    data_keys=sorted(data.keys()),
)
logger.info("##Tool Start - %s", toolname)

tool_notebook = Path(f"/src/{toolname.replace('.ipynb', '')}.ipynb")
if not tool_notebook.exists():
    structured_logger.error(
        "error",
        "Notebook for requested tool was not found",
        tool=toolname,
        notebook=str(tool_notebook),
    )
    logger.error(
        "No notebook found for tool '%s'. Following the config, I expect a notebook called %s inside the container.",
        toolname,
        tool_notebook,
    )
    sys.exit(1)

pm_logger = logging.getLogger("papermill")
pm_logger.setLevel(getattr(logging, os.environ.get("GOTAP_LOG_LEVEL", "INFO").upper()))
pm_logger.handlers = logger.handlers

kwargs = {**vars(params), **data}
pm.execute_notebook(
    tool_notebook,
    Path("/out") / tool_notebook.name,
    parameters=kwargs,
    log_output=True,
)

structured_logger.info(
    "finished",
    "Notebook tool run finished successfully",
    tool=toolname,
    notebook=tool_notebook.name,
)
logger.info("##Tool Finish - %s", toolname)
