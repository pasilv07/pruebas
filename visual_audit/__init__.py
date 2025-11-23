"""
Visual Audit App - Auditoría Visual Competitiva para Campañas Educativas
"""

__version__ = "1.0.0"
__author__ = "Visual Audit System"

from .analyzer import VisualAuditAnalyzer
from .batch_processor import BatchProcessor
from .models import AuditReport

__all__ = ["VisualAuditAnalyzer", "BatchProcessor", "AuditReport"]
