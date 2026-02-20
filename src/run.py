import os
import sys
from datetime import datetime as dt
from pathlib import Path
import papermill as pm
import logging

from parameters import get_parameters, get_data

params = get_parameters()
data = get_data()

toolname = os.environ.get("TOOL_RUN", "foobar").lower()
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
logger.info(f"##Tool Start - {toolname}")

tool_notebook = Path(f"/src/{toolname.replace('.ipynb', '')}.ipynb")
if not tool_notebook.exists():
    logger.error(f"[{dt.now().isocalendar()}] No notebook found for tool '{toolname}'. Following the config, I expect a notebook called {tool_notebook} inside the container.\n")
    sys.exit(1)

pm_logger = logging.getLogger("papermill")
pm_logger.setLevel(getattr(logging, os.environ.get("LOG_LEVEL", "INFO")))
pm_logger.handlers = logger.handlers

kwargs = {**vars(params), **data}
pm.execute_notebook(
    tool_notebook,
    Path("/out") / tool_notebook.name,
    parameters=kwargs,
    log_output=True,
)

logger.info(f"##Tool Finish - {toolname}")
