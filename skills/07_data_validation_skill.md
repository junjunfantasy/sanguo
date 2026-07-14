# Skill 7: Data Validation for Three Kingdoms Knowledge Base

## Overview
This skill covers the validation and quality control of extracted data for the Three Kingdoms knowledge base, including consistency checks, accuracy verification, and completeness assessment.

## Input
- Extracted entities from Skill 2
- Extracted events from Skill 3
- Extracted relationships from Skill 4
- Normalized temporal and spatial data

## Output
- Validated data with quality scores
- Error reports and corrections
- Consistency metrics
- Completeness assessments

## Validation Categories

### 1. Historical Accuracy Validation
- **Source verification**: Cross-reference with historical records
- **Chronological consistency**: Check temporal logic
- **Geographic feasibility**: Verify spatial relationships
- **Entity existence**: Confirm historical figures and locations

### 2. Internal Consistency Validation
- **Entity consistency**: Same entities across different sources
- **Relationship consistency**: No contradictory relationships
- **Temporal consistency**: No temporal paradoxes
- **Spatial consistency**: No geographic impossibilities

### 3. Source Attribution Validation
- **Source tagging**: All data must have source citations
- **Source reliability**: Weight data by source reliability
- **Source conflicts**: Document and resolve conflicts
- **Source coverage**: Ensure adequate source coverage

### 4. Game Data Validation
- **Game balance**: Check card game balance considerations
- **Historical alignment**: Verify game mechanics match history
- **Rule consistency**: Ensure game rules are consistent
- **Version tracking**: Track different game versions

## Validation Rules

### Entity Validation Rules
- **Name uniqueness**: No duplicate entity IDs
- **Name consistency**: Same entity must have consistent naming
- **Attribute completeness**: Core entities must have required attributes
- **Relationship validity**: Relationships must be between existing entities
- **Temporal validity**: Entities must exist during relationship period

### Event Validation Rules
- **Temporal logic**: Events must have valid dates
- **Spatial logic**: Events must have valid locations
- **Participant validity**: Event participants must exist
- **Causal logic**: Causal relationships must be temporally logical
- **Outcome consistency**: Event outcomes must match historical records

### Relationship Validation Rules
- **Symmetry checks**: Certain relationships should be symmetric
- **Transitivity checks**: Certain relationships should be transitive
- **Temporal validity**: Relationships must be temporally valid
- **Cardinality checks**: Relationship types must respect cardinality
- **Source consistency**: Same relationship across sources should agree

### Temporal Validation Rules
- **Date range**: All dates must be within 184-280 AD
- **Chronological order**: Events must be in chronological order
- **Age consistency**: Character ages must be consistent
- **Era accuracy**: Era names must match historical records
- **Relative time**: Relative time references must resolve correctly

### Spatial Validation Rules
- **Geographic existence**: Locations must exist
- **Administrative hierarchy**: Administrative units must be correct
- **Distance feasibility**: Travel distances must be feasible
- **Terrain consistency**: Terrain must match historical descriptions
- **Boundary accuracy**: Political boundaries must be accurate

## Validation Methods

### 1. Automated Validation
- **Schema validation**: Check data against schema definitions
- **Reference validation**: Check foreign key references
- **Range validation**: Check numeric ranges
- **Pattern validation**: Check text patterns

### 2. Cross-Reference Validation
- **Multi-source comparison**: Compare data from different sources
- **Historical record comparison**: Compare with historical records
- **Logical consistency**: Check logical relationships
- **Statistical analysis**: Identify statistical anomalies

### 3. Manual Validation
- **Expert review**: Domain expert review of critical data
- **Source verification**: Direct source verification
- **Context validation**: Validate data in context
- **Edge case handling**: Handle special cases

## Quality Metrics

### Completeness Metrics
- **Entity coverage**: Percentage of known entities extracted
- **Event coverage**: Percentage of known events extracted
- **Relationship coverage**: Percentage of known relationships extracted
- **Attribute coverage**: Percentage of required attributes filled

### Accuracy Metrics
- **Source accuracy**: Percentage of data with reliable sources
- **Validation accuracy**: Percentage of data passing validation
- **Expert accuracy**: Percentage of data confirmed by experts
- **Cross-reference accuracy**: Percentage of data cross-validated

### Consistency Metrics
- **Internal consistency**: Percentage of internally consistent data
- **Source consistency**: Percentage of consistent data across sources
- **Temporal consistency**: Percentage of temporally consistent data
- **Spatial consistency**: Percentage of spatially consistent data

## Error Types and Handling

### 1. Data Entry Errors
- **Typos**: Spelling mistakes in names and attributes
- **Wrong values**: Incorrect attribute values
- **Missing data**: Missing required attributes
- **Format errors**: Incorrect data formats

### 2. Extraction Errors
- **False positives**: Incorrectly extracted entities/events
- **False negatives**: Missed entities/events
- **Attribute errors**: Wrong attribute extraction
- **Relationship errors**: Wrong relationship extraction

### 3. Validation Errors
- **Schema violations**: Data doesn't match schema
- **Reference errors**: Invalid references
- **Logic errors**: Logical inconsistencies
- **Constraint violations**: Constraint violations

### 4. Source Conflicts
- **Contradictory sources**: Different sources disagree
- **Source bias**: Biased source information
- **Source errors**: Errors in source materials
- **Missing sources**: Lack of source information

## Correction Strategies

### 1. Automated Corrections
- **Spelling correction**: Correct common typos
- **Format normalization**: Normalize data formats
- **Default values**: Add default values for missing data
- **Reference resolution**: Resolve broken references

### 2. Semi-Automated Corrections
- **Conflict resolution**: Suggest resolutions for conflicts
- **Data imputation**: Suggest values for missing data
- **Outlier detection**: Flag potential outliers
- **Consistency suggestions**: Suggest consistency improvements

### 3. Manual Corrections
- **Expert review**: Expert review of flagged issues
- **Source verification**: Direct source verification
- **Context analysis**: Analyze context for corrections
- **Decision making**: Make decisions on ambiguous cases

## Output Format

### Validation Report
```json
{
  "validation_id": "unique identifier",
  "validation_date": "ISO date",
  "data_type": "entity/event/relationship",
  "total_records": 1000,
  "valid_records": 950,
  "invalid_records": 50,
  "quality_score": 0.95,
  "errors": [
    {
      "error_id": "unique identifier",
      "error_type": "schema_violation",
      "severity": "high",
      "record_id": "affected record",
      "description": "error description",
      "suggested_correction": "correction suggestion"
    }
  ],
  "metrics": {
    "completeness": 0.92,
    "accuracy": 0.95,
    "consistency": 0.97
  }
}
```

### Quality Score Calculation
```python
quality_score = (completeness * 0.3 + 
                 accuracy * 0.4 + 
                 consistency * 0.3)
```

## Tools and Scripts
- Schema validation libraries
- Cross-reference validation tools
- Statistical analysis packages
- Error reporting systems

## Integration Points
- Validates data from Skills 2-6
- Feeds into knowledge graph construction
- Supports data quality monitoring
- Enables continuous improvement

## Next Steps
After data validation:
- Correct identified errors
- Improve extraction processes
- Update quality metrics
- Establish quality thresholds

## Notes
- Historical accuracy is the highest priority
- Document all validation decisions
- Maintain audit trail of corrections
- Continuously improve validation rules
