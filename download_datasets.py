"""
Dataset Download Helper
Run this script to download the recommended datasets from Kaggle.

Requirements:
  1. Install kaggle: pip install kaggle
  2. Create a Kaggle API token:
     - Go to https://www.kaggle.com/settings → API → Create New Token
     - Place the downloaded kaggle.json in ~/.kaggle/kaggle.json
  3. Run: python download_datasets.py
"""

import os
import subprocess
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASETS_DIR = os.path.join(BASE_DIR, 'datasets')

DATASETS = {
    'mustafa_100k': {
        'kaggle_id': 'iammustafatz/diabetes-prediction-dataset',
        'description': 'Comprehensive Diabetes Prediction Dataset (100k rows)',
    },
    'dtd_multitype': {
        'kaggle_id': 'ankitbatra1210/diabetes-dataset',
        'description': 'Multi-Type Diabetes Dataset (12k rows)',
    },
    'sylhet_symptoms': {
        'kaggle_id': 'ishandutta/early-stage-diabetes-risk-prediction-dataset',
        'description': 'Early-Stage Diabetes Risk Prediction (520 rows)',
    },
}


def download_kaggle_dataset(kaggle_id: str, output_dir: str) -> bool:
    """Download and unzip a Kaggle dataset."""
    os.makedirs(output_dir, exist_ok=True)
    cmd = [
        sys.executable, '-m', 'kaggle', 'datasets', 'download',
        '-d', kaggle_id, '--unzip', '-p', output_dir,
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if result.returncode == 0:
            return True
        else:
            print(f"  Error: {result.stderr.strip()}")
            return False
    except FileNotFoundError:
        print("  Kaggle CLI not found. Install with: pip install kaggle")
        return False
    except subprocess.TimeoutExpired:
        print("  Download timed out.")
        return False


def main():
    # Check kaggle credentials
    kaggle_json = os.path.expanduser('~/.kaggle/kaggle.json')
    if not os.path.exists(kaggle_json):
        print("=" * 60)
        print("  Kaggle API credentials not found!")
        print()
        print("  To download datasets, you need to:")
        print("  1. Go to https://www.kaggle.com/settings")
        print("  2. Scroll to 'API' → click 'Create New Token'")
        print("  3. Place the downloaded kaggle.json in:")
        print(f"     {kaggle_json}")
        print("  4. Re-run this script")
        print("=" * 60)
        return

    os.makedirs(DATASETS_DIR, exist_ok=True)

    for name, info in DATASETS.items():
        output_dir = os.path.join(DATASETS_DIR, name)
        print(f"\n{'='*60}")
        print(f"Downloading: {info['description']}")
        print(f"  Kaggle: {info['kaggle_id']}")
        print(f"  Output: {output_dir}")

        # Check if already downloaded
        if os.listdir(output_dir) if os.path.isdir(output_dir) else []:
            existing = os.listdir(output_dir)
            csv_files = [f for f in existing if f.endswith('.csv')]
            if csv_files:
                print(f"  Already downloaded: {csv_files}")
                continue

        success = download_kaggle_dataset(info['kaggle_id'], output_dir)
        if success:
            files = os.listdir(output_dir)
            print(f"  ✅ Downloaded: {files}")
        else:
            print(f"  ❌ Failed to download")

    print(f"\n{'='*60}")
    print("Done! After downloading, retrain the model:")
    print("  python nn_model.py")
    print("=" * 60)


if __name__ == '__main__':
    main()
