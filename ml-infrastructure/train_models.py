"""
Main training script for medical scan models
Trains models for Brain, Cardiac, Chest, and Bone scans
"""

import os
import sys
import yaml
import argparse
import logging
from pathlib import Path
from typing import Dict, Any

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

from src.training.trainer import train_medical_model
from src.utils.metrics import plot_training_history


def setup_logging(log_level: str = "INFO") -> logging.Logger:
    """Setup logging configuration"""
    
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('training.log')
        ]
    )
    
    return logging.getLogger(__name__)


def load_config(config_path: str) -> Dict[str, Any]:
    """Load configuration from YAML file"""
    
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    return config


def validate_config(config: Dict[str, Any]) -> bool:
    """Validate configuration file"""
    
    required_sections = ['datasets', 'models', 'training', 'hardware']
    
    for section in required_sections:
        if section not in config:
            print(f"Error: Missing required section '{section}' in config")
            return False
    
    # Validate scan types
    scan_types = ['brain', 'cardiac', 'chest', 'bone']
    for scan_type in scan_types:
        if scan_type not in config['datasets']:
            print(f"Error: Missing dataset config for '{scan_type}'")
            return False
    
    return True


def main():
    parser = argparse.ArgumentParser(description='Train medical scan analysis models')
    parser.add_argument('--config', default='config/config.yaml', 
                       help='Path to configuration file')
    parser.add_argument('--scan-type', choices=['brain', 'cardiac', 'chest', 'bone', 'all'],
                       default='all', help='Type of scan to train')
    parser.add_argument('--output-dir', default='models',
                       help='Directory to save trained models')
    parser.add_argument('--log-level', default='INFO',
                       choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
                       help='Logging level')
    parser.add_argument('--resume', type=str, default=None,
                       help='Resume training from checkpoint')
    parser.add_argument('--dry-run', action='store_true',
                       help='Validate config and dataset without training')
    
    args = parser.parse_args()
    
    # Setup logging
    logger = setup_logging(args.log_level)
    
    # Load configuration
    logger.info(f"Loading configuration from {args.config}")
    config = load_config(args.config)
    
    # Validate configuration
    if not validate_config(config):
        logger.error("Configuration validation failed")
        return 1
    
    logger.info("Configuration validated successfully")
    
    # Create output directory
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Determine which scan types to train
    if args.scan_type == 'all':
        scan_types = ['brain', 'cardiac', 'chest', 'bone']
    else:
        scan_types = [args.scan_type]
    
    # Check if datasets exist
    for scan_type in scan_types:
        data_path = config['datasets'][scan_type]['path']
        if not os.path.exists(data_path):
            logger.warning(f"Dataset path does not exist: {data_path}")
            logger.info(f"Please run: python scripts/setup_datasets.py --show-sources")
            logger.info(f"Then organize your data in: {data_path}")
            
            if args.dry_run:
                continue
            else:
                logger.error("Cannot proceed without datasets")
                return 1
    
    if args.dry_run:
        logger.info("Dry run completed successfully")
        return 0
    
    # Train models
    results = {}
    
    for scan_type in scan_types:
        logger.info(f"Starting training for {scan_type} scans...")
        
        try:
            # Create scan-specific output directory
            scan_output_dir = os.path.join(args.output_dir, scan_type)
            os.makedirs(scan_output_dir, exist_ok=True)
            
            # Train model
            result = train_medical_model(
                scan_type=scan_type,
                config=config,
                save_dir=scan_output_dir
            )
            
            results[scan_type] = result
            
            logger.info(f"Training completed for {scan_type}")
            logger.info(f"Test metrics: {result['test_metrics']}")
            
        except Exception as e:
            logger.error(f"Training failed for {scan_type}: {e}")
            results[scan_type] = {'error': str(e)}
    
    # Save training summary
    summary_path = os.path.join(args.output_dir, 'training_summary.yaml')
    with open(summary_path, 'w') as f:
        yaml.dump(results, f, default_flow_style=False)
    
    logger.info(f"Training summary saved to {summary_path}")
    
    # Print final results
    print("\n" + "="*60)
    print("TRAINING SUMMARY")
    print("="*60)
    
    for scan_type, result in results.items():
        if 'error' in result:
            print(f"{scan_type.upper()}: FAILED - {result['error']}")
        else:
            metrics = result['test_metrics']
            print(f"{scan_type.upper()}:")
            print(f"  Accuracy: {metrics['accuracy']:.4f}")
            print(f"  F1 Score: {metrics['f1_score']:.4f}")
            print(f"  Precision: {metrics['precision']:.4f}")
            print(f"  Recall: {metrics['recall']:.4f}")
    
    print("="*60)
    
    return 0


if __name__ == "__main__":
    exit(main())
