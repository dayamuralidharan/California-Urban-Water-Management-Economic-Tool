# California Urban Water Management Economics Tool
California Department of Water Resources Urban Water Management Economics Tool [Development Repository]

License file:
License information.

## Create the executable file for the Streamlit app
- Update CaUWMET/streamlit_executable_builder.spec if needed to configure how the executable is created. 
- Then run the following command from the root directory to create distribution.zip which contains the .exe file and its dependencies.
```sh
.\create-cauwmet-visualizer-executable.ps1
```

## Run the Streamlit app as a .exe file
- Open File Explorer and unzip distribution.zip into a directory of your choosing.
- Double click the streamlit_executable_builder.exe to start the app.
- If you see an error related to socket permissions, try changing the port by setting the CAUWMET_PORT environment variable.
