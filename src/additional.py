import os
import subprocess

def run_script(script_name):
    """Runs the provided script and handles errors."""
    try:
        result = subprocess.run(['python', script_name], check=True, capture_output=True, text=True)
        print(f"Output from {script_name}:\n{result.stdout}")
    except subprocess.CalledProcessError as e:
        print(f"Error running {script_name}: {e.stderr}")

if __name__ == "__main__":
    # Define paths to the four scripts
    base_dir = os.path.dirname(os.path.abspath(__file__))  # Adjust this if needed
    scripts = [
        os.path.join(base_dir, 'generate_additional_data.py'),
        os.path.join(base_dir, 'insert_sales.py')
    ]
    
    # Run each script sequentially
    for script in scripts:
        run_script(script)
