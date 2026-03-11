import chromadb
from chromadb.config import Settings
from typing import List, Dict, Any, Optional
import json
from datetime import datetime

from config import Config
from utils.logger import setup_logger
from utils.helpers import generate_session_id

class VectorStore:
    """
    Vector database for storing and retrieving task history and code
    
    Uses ChromaDB for semantic search of:
    - Previous tasks and solutions
    - Code snippets and patterns
    - Error resolutions
    - Project architectures
    """
    
    def __init__(self):
        """Initialize ChromaDB client and collections"""
        self.logger = setup_logger("VectorStore")
        
        try:
            # Initialize ChromaDB client
            self.client = chromadb.Client(Settings(
                chroma_db_impl="duckdb+parquet",
                persist_directory=Config.CHROMA_DB_PATH
            ))
            
            # Create or get collections
            self.tasks_collection = self.client.get_or_create_collection(
                name="tasks",
                metadata={"description": "Development tasks and their solutions"}
            )
            
            self.code_collection = self.client.get_or_create_collection(
                name="code_snippets",
                metadata={"description": "Code snippets and patterns"}
            )
            
            self.errors_collection = self.client.get_or_create_collection(
                name="error_resolutions",
                metadata={"description": "Error messages and their fixes"}
            )
            
            self.logger.info("Vector store initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize vector store: {str(e)}")
            raise
    
    async def store_task(self,
                        task_id: str,
                        prompt: str,
                        result: Dict[str, Any],
                        session_id: Optional[str] = None) -> bool:
        """
        Store a completed task in vector database
        
        Args:
            task_id: Unique task identifier
            prompt: Original user prompt
            result: Task execution result
            session_id: Session identifier
        
        Returns:
            Success status
        """
        try:
            # Store in tasks collection
            metadata = {
                'task_id': task_id,
                'session_id': session_id or 'default',
                'language': result.get('plan', {}).get('technologies', ['general'])[0],
                'timestamp': datetime.utcnow().isoformat(),
                'success': True
            }
            
            # Create document text combining prompt and summary
            document = f"Task: {prompt}\n\n"
            
            if result.get('plan'):
                document += f"Technologies: {', '.join(result['plan'].get('technologies', []))}\n"
                if result['plan'].get('steps'):
                    document += f"Steps: {len(result['plan']['steps'])}\n"
            
            if result.get('code', {}).get('summary'):
                document += f"\nSummary: {result['code']['summary']}\n"
            
            # Store task
            self.tasks_collection.add(
                documents=[document],
                metadatas=[metadata],
                ids=[task_id]
            )
            
            # Store code snippets separately
            if result.get('code', {}).get('files'):
                await self._store_code_snippets(task_id, result['code']['files'], metadata)
            
            self.logger.info(f"Stored task {task_id} in vector database")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to store task: {str(e)}")
            return False
    
    async def _store_code_snippets(self,
                                   task_id: str,
                                   files: Dict[str, str],
                                   metadata: Dict[str, Any]):
        """Store individual code files as separate documents"""
        try:
            for i, (filename, code) in enumerate(files.items()):
                doc_id = f"{task_id}_file_{i}"
                
                file_metadata = {
                    **metadata,
                    'filename': filename,
                    'file_type': filename.split('.')[-1] if '.' in filename else 'unknown'
                }
                
                # Truncate very long code
                code_truncated = code[:5000] if len(code) > 5000 else code
                
                self.code_collection.add(
                    documents=[code_truncated],
                    metadatas=[file_metadata],
                    ids=[doc_id]
                )
                
        except Exception as e:
            self.logger.warning(f"Failed to store code snippets: {str(e)}")
    
    async def search_similar(self,
                            query: str,
                            limit: int = 5,
                            filter_metadata: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Search for similar tasks
        
        Args:
            query: Search query
            limit: Maximum number of results
            filter_metadata: Optional metadata filters
        
        Returns:
            List of similar tasks
        """
        try:
            # Search tasks collection
            results = self.tasks_collection.query(
                query_texts=[query],
                n_results=limit,
                where=filter_metadata
            )
            
            # Format results
            similar_tasks = []
            
            if results['ids']:
                for i in range(len(results['ids'][0])):
                    similar_tasks.append({
                        'id': results['ids'][0][i],
                        'document': results['documents'][0][i],
                        'metadata': results['metadatas'][0][i],
                        'distance': results['distances'][0][i] if results.get('distances') else None
                    })
            
            self.logger.info(f"Found {len(similar_tasks)} similar tasks")
            return similar_tasks
            
        except Exception as e:
            self.logger.error(f"Search failed: {str(e)}")
            return []
    
    async def search_code(self,
                         query: str,
                         language: Optional[str] = None,
                         limit: int = 5) -> List[Dict[str, Any]]:
        """
        Search for similar code snippets
        
        Args:
            query: Code description or pattern
            language: Filter by programming language
            limit: Maximum results
        
        Returns:
            List of code snippets
        """
        try:
            filter_dict = {'file_type': language} if language else None
            
            results = self.code_collection.query(
                query_texts=[query],
                n_results=limit,
                where=filter_dict
            )
            
            code_snippets = []
            
            if results['ids']:
                for i in range(len(results['ids'][0])):
                    code_snippets.append({
                        'id': results['ids'][0][i],
                        'code': results['documents'][0][i],
                        'metadata': results['metadatas'][0][i],
                        'similarity': 1 - (results['distances'][0][i] if results.get('distances') else 0)
                    })
            
            return code_snippets
            
        except Exception as e:
            self.logger.error(f"Code search failed: {str(e)}")
            return []
    
    async def store_error_resolution(self,
                                     error: str,
                                     solution: str,
                                     language: str,
                                     task_id: str) -> bool:
        """
        Store an error and its resolution
        
        Args:
            error: Error message
            solution: Solution/fix
            language: Programming language
            task_id: Associated task ID
        
        Returns:
            Success status
        """
        try:
            doc_id = f"error_{task_id}_{hash(error) % 10000}"
            
            document = f"Error: {error}\n\nSolution: {solution}"
            
            metadata = {
                'language': language,
                'task_id': task_id,
                'timestamp': datetime.utcnow().isoformat()
            }
            
            self.errors_collection.add(
                documents=[document],
                metadatas=[metadata],
                ids=[doc_id]
            )
            
            self.logger.info(f"Stored error resolution: {doc_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to store error resolution: {str(e)}")
            return False
    
    async def search_error_solutions(self,
                                     error: str,
                                     language: Optional[str] = None,
                                     limit: int = 3) -> List[Dict[str, Any]]:
        """
        Search for solutions to similar errors
        
        Args:
            error: Error message
            language: Programming language filter
            limit: Maximum results
        
        Returns:
            List of similar errors and solutions
        """
        try:
            filter_dict = {'language': language} if language else None
            
            results = self.errors_collection.query(
                query_texts=[error],
                n_results=limit,
                where=filter_dict
            )
            
            solutions = []
            
            if results['ids']:
                for i in range(len(results['ids'][0])):
                    solutions.append({
                        'id': results['ids'][0][i],
                        'resolution': results['documents'][0][i],
                        'metadata': results['metadatas'][0][i]
                    })
            
            return solutions
            
        except Exception as e:
            self.logger.error(f"Error solution search failed: {str(e)}")
            return []
    
    def get_collection_stats(self) -> Dict[str, int]:
        """Get statistics about stored data"""
        try:
            return {
                'tasks': self.tasks_collection.count(),
                'code_snippets': self.code_collection.count(),
                'error_resolutions': self.errors_collection.count()
            }
        except Exception as e:
            self.logger.error(f"Failed to get stats: {str(e)}")
            return {}
    
    def clear_collection(self, collection_name: str) -> bool:
        """Clear a specific collection"""
        try:
            self.client.delete_collection(collection_name)
            self.client.create_collection(collection_name)
            self.logger.info(f"Cleared collection: {collection_name}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to clear collection: {str(e)}")
            return False
