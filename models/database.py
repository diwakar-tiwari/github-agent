from sqlalchemy import Column, String, Integer, Text, DateTime
from sqlalchemy.sql import func
from utils.database import Base

class AnalysisJob(Base):
    __tablename__ = 'analysis_jobs'

    #Primary key
    id = Column(String, primary_key=True)

    # job information
    repo_url = Column(String, nullable=False)
    user_id = Column(String, nullable=False)
    status = Column(String, default='started')  # started, processing, completed, failed

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    #Results
    pdf_path = Column(String, nullable=True)  # Path to the generated PDF report
    error_message = Column(Text, nullable=True)  # Error message if the job fails
    processing_time = Column(Integer, nullable=True)  # Time taken to process the job in seconds

    # Analysis results
    project_docs = Column(Text, nullable=True)
    diagram_meramid = Column(Text, nullable=True)

    def __repr__(self):
        return f"<AnalysisJob(id='{self.id}', status='{self.status}')>"
    
    