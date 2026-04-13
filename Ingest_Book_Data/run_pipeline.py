import subprocess
import sys
import logging

# Set up logging for the master pipeline
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def run_step(command, step_name):
    """Runs a terminal command and stops the pipeline if it fails."""
    logging.info(f"=== Starting {step_name} ===")
    try:
        # Run the command. check=True ensures it raises an error if the script fails.
        subprocess.run(command, check=True)
        logging.info(f"=== Successfully completed {step_name} ===\n")
    except subprocess.CalledProcessError as e:
        logging.error(f"Pipeline halted! Failed during {step_name}.")
        sys.exit(1) # Exit the master script completely

def main():
    logging.info("Starting the full Book ETL Pipeline...\n")

    # sys.executable ensures it uses the exact same Python environment you are currently using
    python_exe = sys.executable

    # Phase 1: Ingest
    run_step([python_exe, "ingest_data.py"], "Phase 1: Data Ingestion")

    # Phase 2: Transform
    run_step([python_exe, "transform_data.py"], "Phase 2: Data Transformation")

    # Phase 3: Dashboard Launch
    logging.info("=== Starting Phase 3: Dashboard Launch ===")
    logging.info("The Streamlit server is starting. It should open automatically in your browser.")
    logging.info("Press Ctrl+C in this terminal when you want to stop the dashboard and exit.\n")
    
    try:
        # Running streamlit using the python module path ensures no "command not found" errors
        subprocess.run([python_exe, "-m", "streamlit", "run", "app_dashboard.py"], check=True)
    except KeyboardInterrupt:
        # Gracefully handle the user pressing Ctrl+C to stop the web server
        logging.info("\nDashboard shut down safely. Pipeline finished!")

if __name__ == "__main__":
    main()