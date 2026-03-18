import yaml
from src.utils_build_ptm_table import process_all_files

def load_config(config_path="config.yaml"):
    """Load YAML configuration file."""
    with open(config_path, "r") as f:
        return yaml.safe_load(f)

def main():
    # Load configuration
    config = load_config()

    input_folder = config["input_folder"]
    output_folder = config["output_folder"]
    separator = config["separator"]

    print("Running preprocessing pipeline with the following settings:")
    print(f"  Input folder: {input_folder}")
    print(f"  Output folder: {output_folder}")
    print(f"  Separator: '{separator}'")

    # Run the pipeline
    process_all_files(
        input_folder=input_folder,
        output_folder=output_folder,
        sep=separator
    )

    print("\nPreprocessing completed successfully.")

if __name__ == "__main__":
    main()
