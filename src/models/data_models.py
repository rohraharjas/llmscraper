from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime
from services.validation_service import DataValidator

@dataclass
class SearchResult:
    """Structure for search results"""
    url: str
    snippet: str
    title: Optional[str] = None
    source: Optional[str] = None
    timestamp: datetime = datetime.now()

@dataclass
class ExtractedInformation:
    """Structure for extracted information"""
    entity: str
    value: str
    confidence: float
    source_urls: List[str]
    extraction_time: datetime = datetime.now()
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            'entity': self.entity,
            'value': self.value,
            'confidence': self.confidence,
            'sources': self.source_urls,
            'timestamp': self.extraction_time.isoformat()
        }

@dataclass
class ProcessingJob:
    """Structure for processing job"""
    job_id: str
    entities: List[str]
    prompt: str
    status: str = 'pending'
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    results: Dict[str, ExtractedInformation] = None
    
    def start(self):
        """Mark job as started"""
        self.status = 'running'
        self.start_time = datetime.now()
    
    def complete(self, results: Dict[str, ExtractedInformation]):
        """Mark job as completed"""
        self.status = 'completed'
        self.end_time = datetime.now()
        self.results = results
    
    def fail(self, error: str):
        """Mark job as failed"""
        self.status = 'failed'
        self.end_time = datetime.now()
        self.error = error

@dataclass
class ExtractionConfig:
    """Configuration for extraction process"""
    prompt_template: str
    info_type: str  # 'email', 'phone', 'text', etc.
    max_results: int = 5
    confidence_threshold: float = 0.7
    timeout: int = 30  # seconds
    
    def validate(self) -> bool:
        """Validate configuration"""
        if not self.prompt_template:
            return False
        if self.max_results < 1:
            return False
        if not (0 < self.confidence_threshold <= 1):
            return False
        if self.timeout < 1:
            return False
        return True

class ExtractionPipeline:
    """Manage the extraction pipeline"""
    
    def __init__(
        self,
        config: ExtractionConfig,
        validator: Optional['DataValidator'] = None
    ):
        self.config = config
        self.validator = validator
        self.jobs: Dict[str, ProcessingJob] = {}
    
    def create_job(
        self,
        entities: List[str],
        prompt: str
    ) -> ProcessingJob:
        """Create new processing job"""
        job_id = datetime.now().strftime('%Y%m%d_%H%M%S')
        job = ProcessingJob(
            job_id=job_id,
            entities=entities,
            prompt=prompt
        )
        self.jobs[job_id] = job
        return job
    
    def get_job_status(self, job_id: str) -> Optional[str]:
        """Get status of specific job"""
        job = self.jobs.get(job_id)
        return job.status if job else None
    
    def get_job_results(
        self,
        job_id: str
    ) -> Optional[Dict[str, ExtractedInformation]]:
        """Get results of specific job"""
        job = self.jobs.get(job_id)
        return job.results if job else None