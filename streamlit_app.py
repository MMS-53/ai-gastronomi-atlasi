"""Streamlit Cloud entrypoint.

The real app lives in frontend-streamlit/app.py. This wrapper keeps local
folder organization intact while making deployment simpler.
"""

from pathlib import Path
import runpy


APP_PATH = Path(__file__).parent / "frontend-streamlit" / "app.py"
runpy.run_path(str(APP_PATH), run_name="__main__")
