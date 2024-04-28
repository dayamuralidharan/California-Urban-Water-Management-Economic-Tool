# Build the executable
Set-Location .\CaUWMET
pyinstaller .\streamlit_executable_builder.spec --clean

# Delete the old distribution folder and distribution.zip 
Set-Location ..
Remove-Item -Recurse -Force distribution
Remove-Item distribution.zip

# Copy the executable and its dependencies to the distribution folder
New-Item distribution -ItemType Directory
Copy-Item CaUWMET/dist/* distribution/ -Recurse
Copy-Item CaUWMET/src distribution/src -Recurse
Copy-Item CaUWMET/app.py distribution/app.py
Copy-Item CaUWMET/graphics distribution/graphics -Recurse
Copy-Item CaUWMET/main.py distribution/main.py

# Create the zip file containing the executable and its dependencies
Compress-Archive distribution distribution.zip