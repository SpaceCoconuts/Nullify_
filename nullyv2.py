import os
import glob
import pandas as pd
import logging

# Configure logging (consistent with stock_processor.py and extract_csv_headers.py)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('fill_blanks.log'),
        logging.StreamHandler()
    ]
)

# Directory containing CSV files
DATA_DIR = "./data"

def fill_blank_cells():
    """Fill blank cells in all CSV files with 'NULL' and preserve leading zeros in Manufacturer Part Number."""
    try:
        # Ensure data directory exists
        if not os.path.exists(DATA_DIR):
            logging.error(f"Directory {DATA_DIR} does not exist")
            return

        # Find all CSV files
        csv_files = glob.glob(os.path.join(DATA_DIR, "*.csv"))
        if not csv_files:
            logging.warning(f"No CSV files found in {DATA_DIR}")
            return

        for csv_file in csv_files:
            try:
                # Read CSV, specifying Manufacturer Part Number as string
                df = pd.read_csv(csv_file, dtype={'Manufacturer Part Number': str})

                # Replace blank cells (NaN, empty strings, None) with 'NULL'
                df = df.fillna('NULL')  # Handles NaN and None
                df = df.replace('', 'NULL')  # Handles empty strings

                # Generate output filename with _cleaned suffix
                base_name = os.path.splitext(csv_file)[0]
                output_file = f"{base_name}_cleaned.csv"

                # Save modified CSV, preserving string format
                df.to_csv(output_file, index=False)
                logging.info(f"Filled blank cells in {csv_file} and saved to {output_file}")

            except Exception as e:
                logging.error(f"Error processing {csv_file}: {e}")
                continue

        logging.info("Completed filling blank cells for all CSV files")

    except Exception as e:
        logging.error(f"Failed to process CSV files: {e}")

if __name__ == "__main__":
    logging.info("Starting blank cell filling process...")
    fill_blank_cells()