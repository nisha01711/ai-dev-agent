import os
import shutil
from pathlib import Path
from typing import Dict, Any, List, Optional
import json

from config import Config
from utils.logger import setup_logger
from utils.validators import validate_file_path
from utils.helpers import sanitize_filename

class FileManager:
    """
    Manages file operations for generated code
    
    Operations:
    - Create files and directories
    - Read file contents
    - Write/update files
    - Delete files/directories
    - List directory contents
    - Project structure management
    """
    
    def __init__(self):
        """Initialize file manager"""
        self.logger = setup_logger("FileManager")
        self.projects_root = Path(Config.PROJECTS_PATH)
        self.projects_root.mkdir(parents=True, exist_ok=True)
        
        self.logger.info(f"File manager initialized with root: {self.projects_root}")
    
    def create_project(self, project_name: str) -> Dict[str, Any]:
        """
        Create a new project directory
        
        Args:
            project_name: Name of the project
        
        Returns:
            Project info
        """
        try:
            safe_name = sanitize_filename(project_name)
            project_path = self.projects_root / safe_name
            
            if project_path.exists():
                return {
                    'success': False,
                    'error': f'Project {safe_name} already exists',
                    'path': None
                }
            
            project_path.mkdir(parents=True, exist_ok=True)
            
            # Create basic structure
            (project_path / 'src').mkdir(exist_ok=True)
            (project_path / 'tests').mkdir(exist_ok=True)
            
            self.logger.info(f"Created project: {safe_name}")
            
            return {
                'success': True,
                'path': str(project_path),
                'name': safe_name
            }
            
        except Exception as e:
            self.logger.error(f"Failed to create project: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'path': None
            }
    
    def create_file(self,
                   project_name: str,
                   file_path: str,
                   content: str,
                   overwrite: bool = False) -> Dict[str, Any]:
        """
        Create a file in project
        
        Args:
            project_name: Project name
            file_path: Relative file path
            content: File content
            overwrite: Overwrite if exists
        
        Returns:
            Operation result
        """
        try:
            # Validate file path for security
            if not validate_file_path(file_path):
                return {
                    'success': False,
                    'error': 'Invalid file path',
                    'path': None
                }
            
            project_path = self.projects_root / sanitize_filename(project_name)
            full_path = project_path / file_path
            
            # Create parent directories
            full_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Check if file exists
            if full_path.exists() and not overwrite:
                return {
                    'success': False,
                    'error': 'File already exists',
                    'path': str(full_path)
                }
            
            # Write file
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.logger.info(f"Created file: {file_path} in {project_name}")
            
            return {
                'success': True,
                'path': str(full_path),
                'size': len(content)
            }
            
        except Exception as e:
            self.logger.error(f"Failed to create file: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'path': None
            }
    
    def create_multiple_files(self,
                             project_name: str,
                             files: Dict[str, str]) -> Dict[str, Any]:
        """
        Create multiple files at once
        
        Args:
            project_name: Project name
            files: Dictionary mapping file paths to content
        
        Returns:
            Operation results
        """
        results = {
            'success': True,
            'files_created': [],
            'files_failed': [],
            'total': len(files)
        }
        
        for file_path, content in files.items():
            result = self.create_file(project_name, file_path, content, overwrite=True)
            
            if result['success']:
                results['files_created'].append(file_path)
            else:
                results['files_failed'].append({
                    'path': file_path,
                    'error': result.get('error')
                })
                results['success'] = False
        
        self.logger.info(f"Created {len(results['files_created'])}/{results['total']} files")
        
        return results
    
    def read_file(self, project_name: str, file_path: str) -> Dict[str, Any]:
        """
        Read file content
        
        Args:
            project_name: Project name
            file_path: Relative file path
        
        Returns:
            File content
        """
        try:
            if not validate_file_path(file_path):
                return {
                    'success': False,
                    'error': 'Invalid file path',
                    'content': None
                }
            
            project_path = self.projects_root / sanitize_filename(project_name)
            full_path = project_path / file_path
            
            if not full_path.exists():
                return {
                    'success': False,
                    'error': 'File not found',
                    'content': None
                }
            
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            return {
                'success': True,
                'content': content,
                'size': len(content),
                'path': str(full_path)
            }
            
        except Exception as e:
            self.logger.error(f"Failed to read file: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'content': None
            }
    
    def delete_file(self, project_name: str, file_path: str) -> Dict[str, Any]:
        """Delete a file"""
        try:
            project_path = self.projects_root / sanitize_filename(project_name)
            full_path = project_path / file_path
            
            if not full_path.exists():
                return {'success': False, 'error': 'File not found'}
            
            full_path.unlink()
            self.logger.info(f"Deleted file: {file_path}")
            
            return {'success': True}
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def list_files(self, project_name: str, subdirectory: str = '') -> Dict[str, Any]:
        """
        List files in project directory
        
        Args:
            project_name: Project name
            subdirectory: Subdirectory to list
        
        Returns:
            File listing
        """
        try:
            project_path = self.projects_root / sanitize_filename(project_name)
            target_path = project_path / subdirectory if subdirectory else project_path
            
            if not target_path.exists():
                return {
                    'success': False,
                    'error': 'Directory not found',
                    'files': [],
                    'directories': []
                }
            
            files = []
            directories = []
            
            for item in target_path.iterdir():
                if item.is_file():
                    files.append({
                        'name': item.name,
                        'size': item.stat().st_size,
                        'modified': item.stat().st_mtime
                    })
                elif item.is_dir():
                    directories.append(item.name)
            
            return {
                'success': True,
                'files': files,
                'directories': directories,
                'path': str(target_path)
            }
            
        except Exception as e:
            self.logger.error(f"Failed to list files: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'files': [],
                'directories': []
            }
    
    def get_project_structure(self, project_name: str) -> Dict[str, Any]:
        """
        Get complete project structure
        
        Args:
            project_name: Project name
        
        Returns:
            Project structure tree
        """
        try:
            project_path = self.projects_root / sanitize_filename(project_name)
            
            if not project_path.exists():
                return {'success': False, 'error': 'Project not found'}
            
            structure = self._build_tree(project_path, project_path)
            
            return {
                'success': True,
                'structure': structure,
                'root': str(project_path)
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _build_tree(self, path: Path, root: Path) -> Dict[str, Any]:
        """Build directory tree recursively"""
        tree = {
            'name': path.name,
            'type': 'directory' if path.is_dir() else 'file',
            'path': str(path.relative_to(root))
        }
        
        if path.is_dir():
            tree['children'] = []
            try:
                for child in sorted(path.iterdir()):
                    tree['children'].append(self._build_tree(child, root))
            except PermissionError:
                pass
        else:
            tree['size'] = path.stat().st_size
        
        return tree
    
    def delete_project(self, project_name: str) -> Dict[str, Any]:
        """Delete entire project"""
        try:
            project_path = self.projects_root / sanitize_filename(project_name)
            
            if not project_path.exists():
                return {'success': False, 'error': 'Project not found'}
            
            shutil.rmtree(project_path)
            self.logger.info(f"Deleted project: {project_name}")
            
            return {'success': True}
            
        except Exception as e:
            self.logger.error(f"Failed to delete project: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def list_projects(self) -> List[Dict[str, Any]]:
        """List all projects"""
        try:
            projects = []
            
            for item in self.projects_root.iterdir():
                if item.is_dir():
                    projects.append({
                        'name': item.name,
                        'path': str(item),
                        'created': item.stat().st_ctime,
                        'modified': item.stat().st_mtime
                    })
            
            return projects
            
        except Exception as e:
            self.logger.error(f"Failed to list projects: {str(e)}")
            return []
    
    def export_project(self, project_name: str, export_path: str) -> Dict[str, Any]:
        """Export project as ZIP"""
        try:
            project_path = self.projects_root / sanitize_filename(project_name)
            
            if not project_path.exists():
                return {'success': False, 'error': 'Project not found'}
            
            # Create ZIP
            shutil.make_archive(
                export_path,
                'zip',
                project_path
            )
            
            return {
                'success': True,
                'archive': f"{export_path}.zip"
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
