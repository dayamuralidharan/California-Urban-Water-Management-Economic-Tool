# Build the executable
Set-Location .\CaUWMET
pyinstaller .\streamlit_executable_builder.spec --clean

# Delete the old distribution folder and distribution.zip 
Set-Location ..
Remove-Item -Recurse -Force streamlitDistribution
Remove-Item streamlitDistribution.zip

# Copy the executable and its dependencies to the distribution folder
New-Item streamlitDistribution -ItemType Directory
Copy-Item CaUWMET/dist/* streamlitDistribution/ -Recurse
Copy-Item CaUWMET/src streamlitDistribution/src -Recurse
Copy-Item CaUWMET/app.py streamlitDistribution/app.py
Copy-Item CaUWMET/graphics streamlitDistribution/graphics -Recurse
Copy-Item CaUWMET/main.py streamlitDistribution/main.py

# Create the zip file containing the executable and its dependencies
Compress-Archive streamlitDistribution streamlitDistribution.zip