import json
from typing import Dict, Any, List, Optional
from datetime import datetime
from pathlib import Path

from config import Config
from utils.logger import setup_logger
from utils.helpers import generate_session_id

class SessionManager:
    """
    Manages user sessions and task history
    
    Tracks:
    - Active sessions
    - Session task history
    - Session metadata
    - Session persistence
    """
    
    def __init__(self):
        """Initialize session manager"""
        self.logger = setup_logger("SessionManager")
        self.sessions: Dict[str, Dict[str, Any]] = {}
        self.session_file = Path(Config.PROJECTS_PATH) / 'sessions.json'
        
        # Load existing sessions
        self._load_sessions()
        
        self.logger.info("Session manager initialized")
    
    def create_session(self, user_id: Optional[str] = None) -> str:
        """
        Create a new session
        
        Args:
            user_id: Optional user identifier
        
        Returns:
            Session ID
        """
        session_id = generate_session_id()
        
        self.sessions[session_id] = {
            'session_id': session_id,
            'user_id': user_id,
            'created_at': datetime.utcnow().isoformat(),
            'last_activity': datetime.utcnow().isoformat(),
            'tasks': [],
            'metadata': {}
        }
        
        self._save_sessions()
        self.logger.info(f"Created session: {session_id}")
        
        return session_id
    
    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """
        Get session data
        
        Args:
            session_id: Session ID
        
        Returns:
            Session data or None
        """
        return self.sessions.get(session_id)
    
    def add_task_to_session(self,
                           session_id: str,
                           task_id: str,
                           task_data: Dict[str, Any]):
        """
        Add a task to session history
        
        Args:
            session_id: Session ID
            task_id: Task ID
            task_data: Task execution data
        """
        if session_id not in self.sessions:
            self.logger.warning(f"Session not found: {session_id}, creating new")
            self.create_session()
        
        session = self.sessions[session_id]
        
        # Add task summary (not full data to save space)
        task_summary = {
            'task_id': task_id,
            'prompt': task_data.get('prompt', ''),
            'language': task_data.get('language', ''),
            'status': task_data.get('status', 'unknown'),
            'timestamp': datetime.utcnow().isoformat(),
            'execution_time': task_data.get('execution_time', 0)
        }
        
        session['tasks'].append(task_summary)
        session['last_activity'] = datetime.utcnow().isoformat()
        
        self._save_sessions()
        self.logger.info(f"Added task {task_id} to session {session_id}")
    
    def get_session_tasks(self, session_id: str) -> List[Dict[str, Any]]:
        """
        Get all tasks for a session
        
        Args:
            session_id: Session ID
        
        Returns:
            List of tasks
        """
        session = self.sessions.get(session_id)
        if not session:
            return []
        
        return session.get('tasks', [])
    
    def update_session_metadata(self,
                                session_id: str,
                                metadata: Dict[str, Any]):
        """
        Update session metadata
        
        Args:
            session_id: Session ID
            metadata: Metadata to update
        """
        if session_id in self.sessions:
            self.sessions[session_id]['metadata'].update(metadata)
            self.sessions[session_id]['last_activity'] = datetime.utcnow().isoformat()
            self._save_sessions()
    
    def delete_session(self, session_id: str) -> bool:
        """
        Delete a session
        
        Args:
            session_id: Session ID
        
        Returns:
            Success status
        """
        if session_id in self.sessions:
            del self.sessions[session_id]
            self._save_sessions()
            self.logger.info(f"Deleted session: {session_id}")
            return True
        
        return False
    
    def get_all_sessions(self) -> List[Dict[str, Any]]:
        """Get all sessions"""
        return list(self.sessions.values())
    
    def cleanup_old_sessions(self, days: int = 30) -> int:
        """
        Cleanup sessions older than specified days
        
        Args:
            days: Age threshold in days
        
        Returns:
            Number of sessions deleted
        """
        from datetime import timedelta
        
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        deleted_count = 0
        
        sessions_to_delete = []
        
        for session_id, session in self.sessions.items():
            last_activity = datetime.fromisoformat(session['last_activity'])
            if last_activity < cutoff_date:
                sessions_to_delete.append(session_id)
        
        for session_id in sessions_to_delete:
            del self.sessions[session_id]
            deleted_count += 1
        
        if deleted_count > 0:
            self._save_sessions()
            self.logger.info(f"Cleaned up {deleted_count} old sessions")
        
        return deleted_count
    
    def _load_sessions(self):
        """Load sessions from file"""
        try:
            if self.session_file.exists():
                with open(self.session_file, 'r') as f:
                    self.sessions = json.load(f)
                self.logger.info(f"Loaded {len(self.sessions)} sessions")
            else:
                self.logger.info("No existing sessions file")
        except Exception as e:
            self.logger.error(f"Failed to load sessions: {str(e)}")
            self.sessions = {}
    
    def _save_sessions(self):
        """Save sessions to file"""
        try:
            self.session_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.session_file, 'w') as f:
                json.dump(self.sessions, f, indent=2)
        except Exception as e:
            self.logger.error(f"Failed to save sessions: {str(e)}")
    
    def get_session_statistics(self, session_id: str) -> Dict[str, Any]:
        """
        Get statistics for a session
        
        Args:
            session_id: Session ID
        
        Returns:
            Session statistics
        """
        session = self.sessions.get(session_id)
        if not session:
            return {}
        
        tasks = session.get('tasks', [])
        
        stats = {
            'total_tasks': len(tasks),
            'successful_tasks': sum(1 for t in tasks if t.get('status') == 'completed'),
            'failed_tasks': sum(1 for t in tasks if t.get('status') == 'failed'),
            'total_execution_time': sum(t.get('execution_time', 0) for t in tasks),
            'languages_used': list(set(t.get('language', '') for t in tasks if t.get('language'))),
            'created_at': session.get('created_at'),
            'last_activity': session.get('last_activity')
        }
        
        return stats
