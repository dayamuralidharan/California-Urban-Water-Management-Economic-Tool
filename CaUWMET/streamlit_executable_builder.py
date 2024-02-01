import subprocess

def run_streamlit():
    command = "streamlit run app.py"
    
    try:
        # Run the command and capture the output
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        
        # Print the output of the command
        print("Command output:", result.stdout)
        
    except subprocess.CalledProcessError as e:
        # Handle errors if the command fails
        print("Error running command:", e)
        print("Command output (if any):", e.output)

if __name__ == "__main__":
    run_streamlit()