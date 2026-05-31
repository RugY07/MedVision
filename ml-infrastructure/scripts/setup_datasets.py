"""
Dataset Setup Script for Medical Scan Analysis
Organizes datasets for Brain, Cardiac, Chest, and Bone scans
"""

import os
import shutil
import pandas as pd
from pathlib import Path
from typing import Dict, List
import argparse
from sklearn.model_selection import train_test_split


def create_dataset_structure(base_dir: str):
    """Create standardized dataset directory structure"""
    
    scan_types = ['brain', 'cardiac', 'chest', 'bone']
    splits = ['train', 'val', 'test']
    
    for scan_type in scan_types:
        for split in splits:
            # Create directory structure
            split_dir = Path(base_dir) / scan_type / split
            split_dir.mkdir(parents=True, exist_ok=True)
            
            print(f"Created directory: {split_dir}")


def organize_dataset(
    source_dir: str,
    target_dir: str,
    scan_type: str,
    test_size: float = 0.2,
    val_size: float = 0.2
):
    """
    Organize raw dataset into train/val/test splits
    
    Expected source structure:
    source_dir/
    ├── class1/
    │   ├── image1.jpg
    │   └── image2.dcm
    └── class2/
        ├── image3.nii
        └── image4.png
    """
    
    source_path = Path(source_dir)
    target_path = Path(target_dir) / scan_type
    
    # Get all classes
    classes = [d.name for d in source_path.iterdir() if d.is_dir()]
    print(f"Found classes: {classes}")
    
    # Collect all images with their labels
    image_data = []
    for class_name in classes:
        class_dir = source_path / class_name
        for image_file in class_dir.rglob('*'):
            if image_file.is_file() and _is_valid_image(image_file):
                image_data.append({
                    'image_path': str(image_file),
                    'class': class_name,
                    'scan_type': scan_type
                })
    
    print(f"Total images found: {len(image_data)}")
    
    # Create DataFrame
    df = pd.DataFrame(image_data)
    
    # Stratified split
    train_df, temp_df = train_test_split(
        df, test_size=(test_size + val_size), 
        stratify=df['class'], random_state=42
    )
    
    val_df, test_df = train_test_split(
        temp_df, test_size=(test_size / (test_size + val_size)),
        stratify=temp_df['class'], random_state=42
    )
    
    # Copy files to organized structure
    for split, split_df in [('train', train_df), ('val', val_df), ('test', test_df)]:
        split_dir = target_path / split
        split_dir.mkdir(parents=True, exist_ok=True)
        
        for _, row in split_df.iterrows():
            # Create class directory
            class_dir = split_dir / row['class']
            class_dir.mkdir(exist_ok=True)
            
            # Copy file
            source_file = Path(row['image_path'])
            target_file = class_dir / source_file.name
            
            try:
                shutil.copy2(source_file, target_file)
            except Exception as e:
                print(f"Error copying {source_file}: {e}")
    
    # Save metadata
    for split, split_df in [('train', train_df), ('val', val_df), ('test', test_df)]:
        metadata_file = target_path / f"{split}_metadata.csv"
        split_df.to_csv(metadata_file, index=False)
        print(f"Saved metadata: {metadata_file}")
    
    print(f"Dataset organization complete for {scan_type}")
    print(f"Train: {len(train_df)}, Val: {len(val_df)}, Test: {len(test_df)}")


def _is_valid_image(file_path: Path) -> bool:
    """Check if file is a valid medical image"""
    valid_extensions = {'.jpg', '.jpeg', '.png', '.dcm', '.nii', '.nii.gz', '.tiff', '.bmp'}
    return file_path.suffix.lower() in valid_extensions or file_path.name.lower().endswith('.nii.gz')


def download_sample_datasets():
    """Download sample datasets for testing (replace with actual dataset sources)"""
    
    # Example dataset sources (you'll need to replace these with actual medical datasets)
    dataset_sources = {
        'brain': {
            'description': 'Brain MRI scans for tumor detection',
            'source': 'https://example.com/brain-dataset',
            'classes': ['normal', 'tumor', 'stroke', 'hemorrhage', 'atrophy'],
            'size': '~5GB'
        },
        'cardiac': {
            'description': 'Cardiac ultrasound and MRI scans',
            'source': 'https://example.com/cardiac-dataset',
            'classes': ['normal', 'cardiomyopathy', 'valvular_disease', 'coronary_disease', 'arrhythmia'],
            'size': '~3GB'
        },
        'chest': {
            'description': 'Chest X-rays and CT scans',
            'source': 'https://example.com/chest-dataset',
            'classes': ['normal', 'pneumonia', 'covid', 'tuberculosis', 'lung_cancer', 'pneumothorax'],
            'size': '~8GB'
        },
        'bone': {
            'description': 'Bone X-rays and MRI scans',
            'source': 'https://example.com/bone-dataset',
            'classes': ['normal', 'fracture', 'osteoporosis', 'arthritis', 'tumor'],
            'size': '~4GB'
        }
    }
    
    print("Sample Dataset Sources (Replace with actual medical datasets):")
    print("=" * 60)
    
    for scan_type, info in dataset_sources.items():
        print(f"\n{scan_type.upper()} SCANS:")
        print(f"Description: {info['description']}")
        print(f"Classes: {', '.join(info['classes'])}")
        print(f"Size: {info['size']}")
        print(f"Source: {info['source']}")
    
    print("\n" + "=" * 60)
    print("IMPORTANT: Replace these placeholder sources with actual medical datasets!")
    print("Consider using datasets like:")
    print("- Brain: BRATS, ADNI, IXI")
    print("- Chest: ChestX-ray14, COVID-19 CT, NIH Chest X-rays")
    print("- Cardiac: EchoNet-Dynamic, Cardiac MRI datasets")
    print("- Bone: MURA, Bone X-ray datasets")


def main():
    parser = argparse.ArgumentParser(description='Setup medical scan datasets')
    parser.add_argument('--base-dir', default='data', help='Base directory for datasets')
    parser.add_argument('--source-dir', help='Source directory with raw data')
    parser.add_argument('--scan-type', choices=['brain', 'cardiac', 'chest', 'bone'], 
                       help='Type of scan to organize')
    parser.add_argument('--create-structure', action='store_true', 
                       help='Create directory structure only')
    parser.add_argument('--show-sources', action='store_true',
                       help='Show sample dataset sources')
    
    args = parser.parse_args()
    
    if args.show_sources:
        download_sample_datasets()
        return
    
    if args.create_structure:
        create_dataset_structure(args.base_dir)
        return
    
    if args.source_dir and args.scan_type:
        organize_dataset(args.source_dir, args.base_dir, args.scan_type)
    else:
        print("Please provide --source-dir and --scan-type for dataset organization")


if __name__ == "__main__":
    main()
