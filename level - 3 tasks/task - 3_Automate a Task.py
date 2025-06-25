#!/usr/bin/env python3
"""
Simple File Organization Automation Script
Uses only Python built-in libraries - no external dependencies required!

This script automates:
1. File organization by type and date
2. Duplicate file detection and handling
3. Report generation with statistics
4. Basic scheduling capability

Author: Automation Script
Date: 2025-06-25
"""

import os
import shutil
import hashlib
import json
import csv
from datetime import datetime
from pathlib import Path
from collections import defaultdict
import argparse
import logging
import threading
import time

class SimpleFileAutomator:
    def __init__(self, config_file=None):
        """Initialize the File Automator with configuration."""
        self.config = self.load_config(config_file)
        self.setup_logging()
        self.stats = {
            'files_processed': 0,
            'files_moved': 0,
            'duplicates_found': 0,
            'errors': 0,
            'start_time': datetime.now()
        }
        
    def load_config(self, config_file):
        """Load configuration from JSON file or use defaults."""
        default_config = {
            'source_directory': './test_source',
            'target_directory': './organized_files',
            'backup_directory': './backup',
            'file_types': {
                'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp'],
                'Documents': ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt'],
                'Spreadsheets': ['.xls', '.xlsx', '.csv', '.ods'],
                'Videos': ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm'],
                'Audio': ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a'],
                'Archives': ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2'],
                'Code': ['.py', '.js', '.html', '.css', '.java', '.cpp', '.c', '.php'],
                'Presentations': ['.ppt', '.pptx', '.odp']
            },
            'organize_by_date': True,
            'handle_duplicates': True,
            'create_backup': False,  # Disabled by default for simplicity
            'generate_report': True,
            'min_file_size_kb': 1  # Skip very small files
        }
        
        if config_file and os.path.exists(config_file):
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    user_config = json.load(f)
                    default_config.update(user_config)
                    print(f"✓ Loaded configuration from {config_file}")
            except Exception as e:
                print(f"⚠ Error loading config: {e}. Using defaults.")
        
        return default_config
    
    def setup_logging(self):
        """Setup logging configuration."""
        log_dir = Path('./logs')
        log_dir.mkdir(exist_ok=True)
        
        # Create a unique log file for this run
        log_filename = f'file_automation_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_dir / log_filename, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        self.logger.info("File Automation Started")
    
    def calculate_file_hash(self, filepath):
        """Calculate MD5 hash of a file for duplicate detection."""
        hash_md5 = hashlib.md5()
        try:
            with open(filepath, "rb") as f:
                for chunk in iter(lambda: f.read(8192), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except Exception as e:
            self.logger.error(f"Error calculating hash for {filepath}: {e}")
            return None
    
    def get_file_category(self, file_extension):
        """Determine file category based on extension."""
        file_ext = file_extension.lower()
        for category, extensions in self.config['file_types'].items():
            if file_ext in extensions:
                return category
        return 'Others'
    
    def create_directory_structure(self, base_path, category, file_date=None):
        """Create organized directory structure."""
        if self.config['organize_by_date'] and file_date:
            year = file_date.strftime('%Y')
            month = file_date.strftime('%m-%B')
            target_path = Path(base_path) / category / year / month
        else:
            target_path = Path(base_path) / category
        
        target_path.mkdir(parents=True, exist_ok=True)
        return target_path
    
    def is_file_too_small(self, file_path):
        """Check if file is too small to process."""
        try:
            size_kb = file_path.stat().st_size / 1024
            return size_kb < self.config['min_file_size_kb']
        except:
            return False
    
    def handle_duplicate(self, source_file, target_file):
        """Handle duplicate files based on configuration."""
        if not self.config['handle_duplicates']:
            return target_file
        
        if target_file.exists():
            source_hash = self.calculate_file_hash(source_file)
            target_hash = self.calculate_file_hash(target_file)
            
            if source_hash and target_hash and source_hash == target_hash:
                self.logger.info(f"🔄 Duplicate found: {source_file.name}")
                self.stats['duplicates_found'] += 1
                return None  # Skip copying
        
        # If not duplicate, create unique filename
        counter = 1
        original_target = target_file
        while target_file.exists():
            name_parts = original_target.stem
            extension = original_target.suffix
            target_file = original_target.parent / f"{name_parts}_copy{counter}{extension}"
            counter += 1
        
        return target_file
    
    def create_backup(self, source_file):
        """Create backup of file before processing."""
        if not self.config['create_backup']:
            return
        
        backup_dir = Path(self.config['backup_directory'])
        backup_dir.mkdir(exist_ok=True)
        
        # Create date-based backup structure
        today = datetime.now().strftime('%Y-%m-%d')
        daily_backup_dir = backup_dir / today
        daily_backup_dir.mkdir(exist_ok=True)
        
        backup_file = daily_backup_dir / source_file.name
        counter = 1
        original_backup = backup_file
        
        while backup_file.exists():
            name_parts = original_backup.stem
            extension = original_backup.suffix
            backup_file = original_backup.parent / f"{name_parts}_backup{counter}{extension}"
            counter += 1
        
        try:
            shutil.copy2(source_file, backup_file)
            self.logger.info(f"💾 Backup created: {backup_file}")
        except Exception as e:
            self.logger.error(f"❌ Error creating backup for {source_file}: {e}")
    
    def organize_files(self):
        """Main file organization function."""
        source_dir = Path(self.config['source_directory'])
        target_dir = Path(self.config['target_directory'])
        
        if not source_dir.exists():
            self.logger.error(f"❌ Source directory does not exist: {source_dir}")
            print(f"Creating example source directory: {source_dir}")
            source_dir.mkdir(parents=True, exist_ok=True)
            
            # Create some example files for testing
            example_files = [
                'example_document.txt',
                'sample_image.jpg',
                'test_data.csv',
                'presentation.pdf'
            ]
            
            for filename in example_files:
                example_file = source_dir / filename
                with open(example_file, 'w') as f:
                    f.write(f"This is a sample {filename} created for testing the automation script.\n")
                    f.write(f"Created on: {datetime.now()}\n")
                    f.write("You can delete this file after testing.\n")
            
            print(f"✓ Created {len(example_files)} example files in {source_dir}")
            print("Run the script again to organize these files!")
            return
        
        target_dir.mkdir(exist_ok=True)
        
        # Get all files from source directory
        all_files = []
        for file_path in source_dir.rglob('*'):
            if file_path.is_file() and not file_path.name.startswith('.'):
                all_files.append(file_path)
        
        if not all_files:
            self.logger.info("ℹ️ No files found to organize")
            return
        
        print(f"📁 Found {len(all_files)} files to process...")
        
        for file_path in all_files:
            try:
                self.stats['files_processed'] += 1
                
                # Skip very small files
                if self.is_file_too_small(file_path):
                    self.logger.info(f"⏭️ Skipping small file: {file_path.name}")
                    continue
                
                # Get file info
                file_extension = file_path.suffix
                file_category = self.get_file_category(file_extension)
                file_date = datetime.fromtimestamp(file_path.stat().st_mtime)
                
                # Create target directory
                target_category_dir = self.create_directory_structure(
                    target_dir, file_category, file_date
                )
                
                # Determine target file path
                target_file_path = target_category_dir / file_path.name
                
                # Handle duplicates
                final_target = self.handle_duplicate(file_path, target_file_path)
                if final_target is None:
                    continue  # Skip duplicate
                
                # Create backup if needed
                self.create_backup(file_path)
                
                # Move file
                shutil.move(str(file_path), str(final_target))
                self.stats['files_moved'] += 1
                self.logger.info(f"📁 Moved: {file_path.name} -> {file_category}/{final_target.name}")
                
                # Progress indicator
                if self.stats['files_processed'] % 10 == 0:
                    print(f"Processed {self.stats['files_processed']} files...")
                
            except Exception as e:
                self.stats['errors'] += 1
                self.logger.error(f"❌ Error processing {file_path}: {e}")
        
        print(f"✅ File organization completed!")
    
    def generate_report(self):
        """Generate comprehensive report of the automation process."""
        if not self.config['generate_report']:
            return
        
        report_dir = Path('./reports')
        report_dir.mkdir(exist_ok=True)
        
        # Calculate processing time
        end_time = datetime.now()
        processing_time = end_time - self.stats['start_time']
        
        # Gather directory statistics
        target_dir = Path(self.config['target_directory'])
        category_stats = defaultdict(int)
        size_stats = defaultdict(int)
        file_types = defaultdict(int)
        
        if target_dir.exists():
            for file_path in target_dir.rglob('*'):
                if file_path.is_file():
                    # Get category from parent directory structure
                    category = 'Others'
                    for part in file_path.parts:
                        if part in self.config['file_types']:
                            category = part
                            break
                    
                    category_stats[category] += 1
                    file_types[file_path.suffix.lower()] += 1
                    
                    try:
                        size_stats[category] += file_path.stat().st_size
                    except:
                        pass
        
        # Create comprehensive report data
        report_data = {
            'execution_summary': {
                'execution_date': end_time.strftime('%Y-%m-%d %H:%M:%S'),
                'processing_time_seconds': processing_time.total_seconds(),
                'processing_time_formatted': str(processing_time),
                'source_directory': str(self.config['source_directory']),
                'target_directory': str(self.config['target_directory'])
            },
            'statistics': self.stats.copy(),
            'category_breakdown': dict(category_stats),
            'file_type_breakdown': dict(file_types),
            'size_breakdown_mb': {k: round(v/1024/1024, 2) for k, v in size_stats.items()},
            'configuration_used': self.config
        }
        
        # Remove datetime object for JSON serialization
        report_data['statistics']['start_time'] = self.stats['start_time'].strftime('%Y-%m-%d %H:%M:%S')
        
        # Save JSON report
        timestamp = end_time.strftime("%Y%m%d_%H%M%S")
        json_report_file = report_dir / f'automation_report_{timestamp}.json'
        
        try:
            with open(json_report_file, 'w', encoding='utf-8') as f:
                json.dump(report_data, f, indent=2, ensure_ascii=False)
            self.logger.info(f"📊 JSON report saved: {json_report_file}")
        except Exception as e:
            self.logger.error(f"Error saving JSON report: {e}")
        
        # Save CSV summary
        csv_report_file = report_dir / f'summary_{timestamp}.csv'
        try:
            with open(csv_report_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                
                # Summary section
                writer.writerow(['=== EXECUTION SUMMARY ==='])
                writer.writerow(['Metric', 'Value'])
                writer.writerow(['Execution Date', report_data['execution_summary']['execution_date']])
                writer.writerow(['Processing Time', report_data['execution_summary']['processing_time_formatted']])
                writer.writerow(['Source Directory', report_data['execution_summary']['source_directory']])
                writer.writerow(['Target Directory', report_data['execution_summary']['target_directory']])
                
                writer.writerow([])
                writer.writerow(['=== PROCESSING STATISTICS ==='])
                writer.writerow(['Files Processed', self.stats['files_processed']])
                writer.writerow(['Files Moved', self.stats['files_moved']])
                writer.writerow(['Duplicates Found', self.stats['duplicates_found']])
                writer.writerow(['Errors', self.stats['errors']])
                
                writer.writerow([])
                writer.writerow(['=== CATEGORY BREAKDOWN ==='])
                writer.writerow(['Category', 'File Count', 'Size (MB)'])
                for category in sorted(category_stats.keys()):
                    size_mb = round(size_stats[category]/1024/1024, 2) if category in size_stats else 0
                    writer.writerow([category, category_stats[category], size_mb])
                
                writer.writerow([])
                writer.writerow(['=== FILE TYPE BREAKDOWN ==='])
                writer.writerow(['File Extension', 'Count'])
                for ext in sorted(file_types.keys()):
                    writer.writerow([ext if ext else 'No Extension', file_types[ext]])
            
            self.logger.info(f"📈 CSV report saved: {csv_report_file}")
        except Exception as e:
            self.logger.error(f"Error saving CSV report: {e}")
        
        # Print summary to console
        print("\n" + "="*60)
        print("📊 AUTOMATION SUMMARY")
        print("="*60)
        print(f"⏱️  Processing Time: {processing_time}")
        print(f"📄 Files Processed: {self.stats['files_processed']}")
        print(f"📁 Files Moved: {self.stats['files_moved']}")
        print(f"🔄 Duplicates Found: {self.stats['duplicates_found']}")
        print(f"❌ Errors: {self.stats['errors']}")
        
        if category_stats:
            print(f"\n📂 Category Breakdown:")
            for category, count in sorted(category_stats.items()):
                size_mb = round(size_stats[category]/1024/1024, 2) if category in size_stats else 0
                print(f"   {category}: {count} files ({size_mb} MB)")
        
        print(f"\n📋 Reports saved in: {report_dir}")
        print("="*60)
    
    def run(self):
        """Execute the complete automation process."""
        self.logger.info("🚀 Starting file automation process")
        print("🚀 File Automation Started")
        
        try:
            self.organize_files()
            self.generate_report()
            
            print("✅ Automation completed successfully!")
            
        except Exception as e:
            self.logger.error(f"💥 Automation failed: {e}")
            print(f"❌ Automation failed: {e}")
            raise

def create_sample_config():
    """Create a sample configuration file."""
    config = {
        "source_directory": "./test_source",
        "target_directory": "./organized_files",
        "backup_directory": "./backup",
        "organize_by_date": True,
        "handle_duplicates": True,
        "create_backup": False,
        "generate_report": True,
        "min_file_size_kb": 1,
        "file_types": {
            "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp"],
            "Documents": [".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt"],
            "Spreadsheets": [".xls", ".xlsx", ".csv", ".ods"],
            "Videos": [".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv", ".webm"],
            "Audio": [".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a"],
            "Archives": [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2"],
            "Code": [".py", ".js", ".html", ".css", ".java", ".cpp", ".c", ".php"],
            "Presentations": [".ppt", ".pptx", ".odp"]
        }
    }
    
    config_file = 'file_automation_config.json'
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Sample configuration file created: {config_file}")
    print("📝 Edit this file to customize your automation settings")

def simple_scheduler(config_file=None, interval_hours=24):
    """Simple scheduler using threading - no external dependencies."""
    def run_automation():
        automator = SimpleFileAutomator(config_file)
        automator.run()
    
    def scheduler_loop():
        while True:
            try:
                print(f"\n⏰ Running scheduled automation...")
                run_automation()
                print(f"✅ Automation completed. Next run in {interval_hours} hours.")
                time.sleep(interval_hours * 3600)  # Convert hours to seconds
            except KeyboardInterrupt:
                print("\n🛑 Scheduler stopped by user")
                break
            except Exception as e:
                print(f"❌ Error in scheduled run: {e}")
                print("⏳ Waiting 5 minutes before retry...")
                time.sleep(300)  # Wait 5 minutes before retry
    
    # Run once immediately
    print("🚀 Running initial automation...")
    run_automation()
    
    print(f"\n⏰ Scheduler started - automation will run every {interval_hours} hours")
    print("Press Ctrl+C to stop the scheduler")
    
    try:
        scheduler_loop()
    except KeyboardInterrupt:
        print("\n🛑 Scheduler stopped")

def main():
    """Main function with command-line interface."""
    parser = argparse.ArgumentParser(
        description='Simple File Organization Automation Script',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python file_automator.py                    # Run once with default settings
  python file_automator.py --create-config   # Create configuration file
  python file_automator.py --config my.json  # Use custom configuration
  python file_automator.py --schedule 6      # Run every 6 hours
        """
    )
    
    parser.add_argument('--config', '-c', 
                       help='Path to configuration file (JSON format)')
    parser.add_argument('--create-config', action='store_true',
                       help='Create sample configuration file and exit')
    parser.add_argument('--schedule', '-s', type=int, metavar='HOURS',
                       help='Run automation on schedule (specify interval in hours)')
    
    args = parser.parse_args()
    
    if args.create_config:
        create_sample_config()
        return
    
    if args.schedule:
        simple_scheduler(args.config, args.schedule)
        return
    
    # Default: run once
    automator = SimpleFileAutomator(args.config)
    automator.run()

if __name__ == "__main__":
    main()