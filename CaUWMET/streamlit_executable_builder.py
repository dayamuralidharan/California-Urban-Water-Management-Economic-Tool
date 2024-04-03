import logging
import traceback
import streamlit
import streamlit.web.cli as stcli
import os, sys


def resolve_path(path):
    resolved_path = os.path.abspath(os.path.join(os.getcwd(), path))
    return resolved_path


if __name__ == "__main__":
    try:
        logging.basicConfig(filename = 'logfile.log', filemode = 'w', level = logging.INFO)

        logging.info("Running streamlit app....")
        sys.argv = [
            "streamlit",
            "run",
            resolve_path("app.py"),
            "--global.developmentMode=false",
        ]
        sys.exit(stcli.main())
    except Exception as exception:
        logging.error(traceback.format_exc())