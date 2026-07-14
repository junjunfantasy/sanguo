#!/usr/bin/env python3
"""
Three Kingdoms Text Preprocessor
Handles text preprocessing for historical and literary sources
"""

import re
import json
from pathlib import Path
from typing import List, Dict, Tuple
from dataclasses import dataclass


@dataclass
class TextSegment:
    """Represents a processed text segment"""
    content: str
    source: str
    chapter: str
    segment_id: str
    metadata: Dict


class ThreeKingdomsPreprocessor:
    """Main preprocessor for Three Kingdoms texts"""
    
    def __init__(self, data_dir: Path):
        self.data_dir = data_dir
        self.historical_dir = data_dir / "historical"
        self.literary_dir = data_dir / "literary"
        
    def load_text(self, source: str, filename: str) -> str:
        """Load text from file"""
        if source == "historical":
            filepath = self.historical_dir / source / filename
        else:
            filepath = self.literary_dir / source / filename
            
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters but keep Chinese punctuation
        text = re.sub(r'[^\u4e00-\u9fff\u3000-\u303f\uff00-\uffef\s]', '', text)
        # Normalize punctuation
        text = text.replace('，', '，').replace('。', '。')
        return text.strip()
    
    def segment_by_chapter(self, text: str, source: str) -> List[TextSegment]:
        """Segment text by chapters"""
        segments = []
        
        if source == "sanguozhi":
            segments = self._segment_sanguozhi(text)
        elif source == "sanguoyanyi":
            segments = self._segment_sanguoyanyi(text)
        else:
            segments = self._segment_generic(text, source)
            
        return segments
    
    def _segment_sanguozhi(self, text: str) -> List[TextSegment]:
        """Segment Records of Three Kingdoms by book and chapter"""
        segments = []
        # Sanguozhi is divided into Wei, Shu, Wu books
        pattern = r'(魏书|蜀书|吴书)(.*?)(?=(魏书|蜀书|吴书|$))'
        matches = re.finditer(pattern, text, re.DOTALL)
        
        for i, match in enumerate(matches):
            book = match.group(1)
            content = match.group(2)
            segment = TextSegment(
                content=content.strip(),
                source="sanguozhi",
                chapter=book,
                segment_id=f"sanguozhi_{book}_{i}",
                metadata={"book": book, "type": "historical"}
            )
            segments.append(segment)
            
        return segments
    
    def _segment_sanguoyanyi(self, text: str) -> List[TextSegment]:
        """Segment Romance of Three Kingdoms by chapters (120 chapters)"""
        segments = []
        # Pattern for chapter headers: "第X回"
        pattern = r'第(\d+)回(.*?)(?=第\d+回|$)'
        matches = re.finditer(pattern, text, re.DOTALL)
        
        for match in matches:
            chapter_num = match.group(1)
            content = match.group(2)
            segment = TextSegment(
                content=content.strip(),
                source="sanguoyanyi",
                chapter=f"第{chapter_num}回",
                segment_id=f"sanguoyanyi_chapter_{chapter_num}",
                metadata={"chapter": chapter_num, "type": "literary"}
            )
            segments.append(segment)
            
        return segments
    
    def _segment_generic(self, text: str, source: str) -> List[TextSegment]:
        """Generic segmentation for other sources"""
        # Split by paragraphs or sections
        paragraphs = text.split('\n\n')
        segments = []
        
        for i, para in enumerate(paragraphs):
            if len(para.strip()) > 10:  # Filter out very short segments
                segment = TextSegment(
                    content=para.strip(),
                    source=source,
                    chapter=f"section_{i}",
                    segment_id=f"{source}_section_{i}",
                    metadata={"type": "generic"}
                )
                segments.append(segment)
                
        return segments
    
    def extract_sentences(self, segment: TextSegment) -> List[str]:
        """Extract sentences from a text segment"""
        # Chinese sentence segmentation
        sentences = re.split(r'[。！？；]', segment.content)
        return [s.strip() for s in sentences if len(s.strip()) > 5]
    
    def add_source_tags(self, text: str, source: str) -> str:
        """Add source tags to text for tracking"""
        return f"[{source}] {text}"
    
    def process_pipeline(self, source_files: List[Tuple[str, str]]) -> List[TextSegment]:
        """Main processing pipeline"""
        all_segments = []
        
        for source, filename in source_files:
            print(f"Processing {source}/{filename}...")
            
            # Load text
            raw_text = self.load_text(source, filename)
            
            # Clean text
            clean_text = self.clean_text(raw_text)
            
            # Segment by chapter
            segments = self.segment_by_chapter(clean_text, source)
            
            all_segments.extend(segments)
            
        return all_segments
    
    def save_segments(self, segments: List[TextSegment], output_path: Path):
        """Save processed segments to JSON"""
        output_data = []
        for segment in segments:
            output_data.append({
                "content": segment.content,
                "source": segment.source,
                "chapter": segment.chapter,
                "segment_id": segment.segment_id,
                "metadata": segment.metadata
            })
            
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)


def main():
    """Main execution function"""
    data_dir = Path("/Users/macbook/AI/sanguo/data")
    preprocessor = ThreeKingdomsPreprocessor(data_dir)
    
    # Define source files to process
    source_files = [
        # Historical sources
        ("historical/sanguozhi", "weishu.txt"),
        ("historical/sanguozhi", "shushu.txt"),
        ("historical/sanguozhi", "wushu.txt"),
        # Literary sources
        ("literary/sanguoyanyi", "sanguoyanyi.txt"),
    ]
    
    # Process texts
    segments = preprocessor.process_pipeline(source_files)
    
    # Save results
    output_path = Path("/Users/macbook/AI/sanguo/kg/processed_segments.json")
    preprocessor.save_segments(segments, output_path)
    
    print(f"Processed {len(segments)} segments")
    print(f"Output saved to {output_path}")


if __name__ == "__main__":
    main()
