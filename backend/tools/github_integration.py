from github import Github, GithubException
from typing import Dict, Any, Optional, List
from pathlib import Path
import tempfile
import os

from config import Config
from utils.logger import setup_logger

class GitHubIntegration:
    """
    GitHub integration for repository management
    
    Features:
    - Create repositories
    - Push code to GitHub
    - Create pull requests
    - Manage branches
    - Repository analysis
    """
    
    def __init__(self):
        """Initialize GitHub client"""
        self.logger = setup_logger("GitHubIntegration")
        
        try:
            if not Config.GITHUB_TOKEN:
                self.logger.warning("GitHub token not configured")
                self.client = None
            else:
                self.client = Github(Config.GITHUB_TOKEN)
                self.user = self.client.get_user()
                self.logger.info(f"GitHub integration initialized for user: {self.user.login}")
        except Exception as e:
            self.logger.error(f"Failed to initialize GitHub client: {str(e)}")
            self.client = None
    
    def create_repository(self,
                         name: str,
                         description: str = "",
                         private: bool = False,
                         auto_init: bool = True) -> Dict[str, Any]:
        """
        Create a new GitHub repository
        
        Args:
            name: Repository name
            description: Repository description
            private: Make repository private
            auto_init: Initialize with README
        
        Returns:
            Repository information
        """
        if not self.client:
            return {
                'success': False,
                'error': 'GitHub not configured',
                'url': None
            }
        
        try:
            repo = self.user.create_repo(
                name=name,
                description=description,
                private=private,
                auto_init=auto_init
            )
            
            self.logger.info(f"Created repository: {repo.html_url}")
            
            return {
                'success': True,
                'url': repo.html_url,
                'clone_url': repo.clone_url,
                'name': repo.name,
                'full_name': repo.full_name
            }
            
        except GithubException as e:
            self.logger.error(f"Failed to create repository: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'url': None
            }
    
    def push_code(self,
                 repo_name: str,
                 files: Dict[str, str],
                 branch: str = "main",
                 commit_message: str = "Add generated code") -> Dict[str, Any]:
        """
        Push code files to repository
        
        Args:
            repo_name: Repository name (format: username/repo or just repo)
            files: Dictionary mapping file paths to content
            branch: Target branch
            commit_message: Commit message
        
        Returns:
            Operation result
        """
        if not self.client:
            return {'success': False, 'error': 'GitHub not configured'}
        
        try:
            # Get repository
            if '/' not in repo_name:
                repo_name = f"{self.user.login}/{repo_name}"
            
            repo = self.client.get_repo(repo_name)
            
            # Push each file
            created_files = []
            failed_files = []
            
            for file_path, content in files.items():
                try:
                    # Check if file exists
                    try:
                        existing_file = repo.get_contents(file_path, ref=branch)
                        # Update existing file
                        repo.update_file(
                            path=file_path,
                            message=f"Update {file_path}",
                            content=content,
                            sha=existing_file.sha,
                            branch=branch
                        )
                    except GithubException:
                        # Create new file
                        repo.create_file(
                            path=file_path,
                            message=f"Add {file_path}",
                            content=content,
                            branch=branch
                        )
                    
                    created_files.append(file_path)
                    
                except Exception as e:
                    self.logger.error(f"Failed to push {file_path}: {str(e)}")
                    failed_files.append({'path': file_path, 'error': str(e)})
            
            self.logger.info(f"Pushed {len(created_files)} files to {repo_name}")
            
            return {
                'success': len(failed_files) == 0,
                'files_created': created_files,
                'files_failed': failed_files,
                'repo_url': repo.html_url
            }
            
        except Exception as e:
            self.logger.error(f"Failed to push code: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def create_pull_request(self,
                           repo_name: str,
                           title: str,
                           body: str,
                           head: str,
                           base: str = "main") -> Dict[str, Any]:
        """
        Create a pull request
        
        Args:
            repo_name: Repository name
            title: PR title
            body: PR description
            head: Source branch
            base: Target branch
        
        Returns:
            PR information
        """
        if not self.client:
            return {'success': False, 'error': 'GitHub not configured'}
        
        try:
            if '/' not in repo_name:
                repo_name = f"{self.user.login}/{repo_name}"
            
            repo = self.client.get_repo(repo_name)
            
            pr = repo.create_pull(
                title=title,
                body=body,
                head=head,
                base=base
            )
            
            self.logger.info(f"Created PR: {pr.html_url}")
            
            return {
                'success': True,
                'url': pr.html_url,
                'number': pr.number,
                'title': pr.title
            }
            
        except Exception as e:
            self.logger.error(f"Failed to create PR: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def create_branch(self,
                     repo_name: str,
                     branch_name: str,
                     from_branch: str = "main") -> Dict[str, Any]:
        """Create a new branch"""
        if not self.client:
            return {'success': False, 'error': 'GitHub not configured'}
        
        try:
            if '/' not in repo_name:
                repo_name = f"{self.user.login}/{repo_name}"
            
            repo = self.client.get_repo(repo_name)
            
            # Get the source branch
            source = repo.get_branch(from_branch)
            
            # Create new branch reference
            ref = repo.create_git_ref(
                ref=f"refs/heads/{branch_name}",
                sha=source.commit.sha
            )
            
            self.logger.info(f"Created branch: {branch_name}")
            
            return {
                'success': True,
                'branch': branch_name,
                'sha': source.commit.sha
            }
            
        except Exception as e:
            self.logger.error(f"Failed to create branch: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_repository_info(self, repo_name: str) -> Dict[str, Any]:
        """Get repository information"""
        if not self.client:
            return {'success': False, 'error': 'GitHub not configured'}
        
        try:
            if '/' not in repo_name:
                repo_name = f"{self.user.login}/{repo_name}"
            
            repo = self.client.get_repo(repo_name)
            
            return {
                'success': True,
                'name': repo.name,
                'full_name': repo.full_name,
                'description': repo.description,
                'url': repo.html_url,
                'clone_url': repo.clone_url,
                'language': repo.language,
                'stars': repo.stargazers_count,
                'forks': repo.forks_count,
                'open_issues': repo.open_issues_count,
                'default_branch': repo.default_branch,
                'created_at': repo.created_at.isoformat(),
                'updated_at': repo.updated_at.isoformat()
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def list_repositories(self, limit: int = 10) -> List[Dict[str, Any]]:
        """List user's repositories"""
        if not self.client:
            return []
        
        try:
            repos = self.user.get_repos(sort='updated', direction='desc')
            
            repo_list = []
            for repo in repos[:limit]:
                repo_list.append({
                    'name': repo.name,
                    'full_name': repo.full_name,
                    'description': repo.description,
                    'url': repo.html_url,
                    'language': repo.language,
                    'stars': repo.stargazers_count,
                    'private': repo.private
                })
            
            return repo_list
            
        except Exception as e:
            self.logger.error(f"Failed to list repositories: {str(e)}")
            return []
    
    def is_configured(self) -> bool:
        """Check if GitHub is properly configured"""
        return self.client is not None
