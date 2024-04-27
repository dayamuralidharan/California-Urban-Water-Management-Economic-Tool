import logging
import traceback
import streamlit
import streamlit.web.cli as stcli
import os, sys

def getPort() -> str:
    if 'CAUWMET_PORT' in os.environ:
        return os.environ['CAUWMET_PORT']
    return "8080"

def resolve_path(path: str) -> str:
    return os.path.abspath(os.path.join(os.getcwd(), path))

if __name__ == "__main__":
    try:
        port = getPort()
        logging.basicConfig(filename = 'logfile.log', filemode = 'w', level = logging.INFO)
        logging.info("Running streamlit app on port %s", port)
        sys.argv = [
            "streamlit",
            "run",
            resolve_path("app.py"),
            "--global.developmentMode=false",
            "--server.port={}".format(port)
        ]
        sys.exit(stcli.main())
    except Exception as exception:
        logging.error(traceback.format_exc())

