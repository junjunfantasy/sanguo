# Skill 8: Knowledge Graph Construction for Three Kingdoms Knowledge Base

## Overview
This skill covers the construction of the knowledge graph for the Three Kingdoms knowledge base, including entity nodes, relationship edges, and graph schema definition.

## Input
- Validated entities from Skill 2
- Validated events from Skill 3
- Validated relationships from Skill 4
- Normalized temporal and spatial data

## Output
- Knowledge graph database (Neo4j or similar)
- Graph schema and ontology
- Graph statistics and metrics
- Query interfaces and APIs

## Graph Schema Design

### Node Types (Entity Nodes)
```cypher
// Character Node
(:Character {
  entity_id: String,
  name: String,
  aliases: [String],
  style_name: String,
  birth_year: Integer,
  death_year: Integer,
  faction: String,
  strength: Integer,
  intelligence: Integer,
  political: Integer,
  historical_source: String
})

// Location Node
(:Location {
  entity_id: String,
  ancient_name: String,
  modern_name: String,
  coordinates: {lat: Float, lon: Float},
  administrative_level: String,
  strategic_value: String
})

// Event Node
(:Event {
  entity_id: String,
  name: String,
  event_type: String,
  date_ad: Integer,
  era_date: String,
  location: String,
  description: String,
  outcome: String
})

// Faction Node
(:Faction {
  entity_id: String,
  name: String,
  ruler: String,
  period_start: Integer,
  period_end: Integer,
  territory: [String]
})
```

### Edge Types (Relationship Edges)
```cypher
// Blood Relationships
(:Character)-[:BLOOD_RELATION {type: "father"}]->(:Character)
(:Character)-[:BLOOD_RELATION {type: "spouse"}]->(:Character)

// Political Relationships
(:Character)-[:POLITICAL_RELATION {type: "ruler_subject"}]->(:Character)
(:Character)-[:POLITICAL_RELATION {type: "ally"}]->(:Character)

// Military Relationships
(:Character)-[:MILITARY_RELATION {type: "commander"}]->(:Character)
(:Character)-[:MILITARY_RELATION {type: "enemy"}]->(:Character)

// Event Participation
(:Character)-[:PARTICIPATED_IN]->(:Event)
(:Event)-[:OCCURRED_AT]->(:Location)
(:Event)-[:BELONGS_TO_FACTION]->(:Faction)

// Geographic Relationships
(:Location)-[:ADMINISTRATIVE_HIERARCHY]->(:Location)
(:Location)-[:BORDERS]->(:Location)

// Temporal Relationships
(:Event)-[:TEMPORAL_RELATION {type: "before"}]->(:Event)
(:Event)-[:CAUSAL_RELATION]->(:Event)
```

## Graph Construction Process

### 1. Node Creation
- **Entity nodes**: Create nodes for all validated entities
- **Attribute assignment**: Assign attributes from validated data
- **Index creation**: Create indexes for frequently queried properties
- **Constraint creation**: Create uniqueness constraints

### 2. Edge Creation
- **Relationship edges**: Create edges for validated relationships
- **Property assignment**: Assign relationship properties
- **Direction assignment**: Assign appropriate edge directions
- **Multiplicity handling**: Handle multiple relationships between same nodes

### 3. Graph Enrichment
- **Derived relationships**: Create relationships inferred from data
- **Graph metrics**: Calculate centrality and other metrics
- **Community detection**: Identify communities and clusters
- **Path analysis**: Enable path-based queries

### 4. Graph Optimization
- **Index optimization**: Optimize indexes for query performance
- **Memory optimization**: Optimize memory usage
- **Query optimization**: Optimize common query patterns
- **Partitioning**: Partition large graphs if necessary

## Graph Construction Tools

### Neo4j Implementation
```python
from neo4j import GraphDatabase

class ThreeKingdomsGraphBuilder:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
    
    def create_character_node(self, character_data):
        with self.driver.session() as session:
            session.run("""
                CREATE (c:Character {
                    entity_id: $entity_id,
                    name: $name,
                    aliases: $aliases,
                    style_name: $style_name,
                    birth_year: $birth_year,
                    death_year: $death_year,
                    faction: $faction,
                    strength: $strength,
                    intelligence: $intelligence,
                    political: $political
                })
            """, **character_data)
    
    def create_relationship(self, source_id, target_id, rel_type, properties):
        with self.driver.session() as session:
            session.run("""
                MATCH (a {entity_id: $source_id})
                MATCH (b {entity_id: $target_id})
                CREATE (a)-[r:RELATIONSHIP {type: $rel_type, **$properties}]->(b)
            """, source_id=source_id, target_id=target_id, 
                 rel_type=rel_type, properties=properties)
```

### NetworkX Implementation (Alternative)
```python
import networkx as nx

class ThreeKingdomsNetworkBuilder:
    def __init__(self):
        self.graph = nx.MultiDiGraph()
    
    def add_entity_node(self, entity_data):
        self.graph.add_node(entity_data['entity_id'], **entity_data)
    
    def add_relationship_edge(self, source, target, rel_type, properties):
        self.graph.add_edge(source, target, relation=rel_type, **properties)
```

## Graph Statistics and Metrics

### Node Statistics
- **Total nodes**: Count of all nodes
- **Node types**: Count by node type
- **Node degrees**: Degree distribution
- **Node centrality**: Various centrality measures

### Edge Statistics
- **Total edges**: Count of all edges
- **Edge types**: Count by edge type
- **Edge weights**: Weight distribution
- **Edge reciprocity**: Reciprocity measures

### Graph Metrics
- **Density**: Graph density
- **Clustering coefficient**: Clustering measures
- **Path lengths**: Average path length
- **Connected components**: Component analysis

### Domain-Specific Metrics
- **Faction size**: Size of each faction
- **Character influence**: Influence measures for characters
- **Event importance**: Importance measures for events
- **Location centrality**: Centrality of locations

## Query Patterns

### Character Queries
```cypher
// Find all relationships of a character
MATCH (c:Character {name: "刘备"})-[r]-(other)
RETURN c, r, other

// Find characters in same faction
MATCH (c:Character {faction: "蜀"})-[:POLITICAL_RELATION]->(other)
RETURN c, other

// Find most influential characters
MATCH (c:Character)
RETURN c.name, size((c)-[]-()) as connections
ORDER BY connections DESC
LIMIT 10
```

### Event Queries
```cypher
// Find events in a time period
MATCH (e:Event)
WHERE e.date_ad >= 200 AND e.date_ad <= 210
RETURN e

// Find events at a location
MATCH (e:Event)-[:OCCURRED_AT]->(l:Location {ancient_name: "赤壁"})
RETURN e

// Find causal event chains
MATCH path = (e1:Event)-[:CAUSAL_RELATION*]->(e2:Event)
RETURN path
```

### Relationship Queries
```cypher
// Find shortest path between characters
MATCH path = shortestPath((c1:Character {name: "刘备"})-[*]-(c2:Character {name: "曹操"}))
RETURN path

// Find all enemies of a character
MATCH (c:Character {name: "刘备"})-[:MILITARY_RELATION {type: "enemy"}]->(enemy)
RETURN enemy

// Find family relationships
MATCH (c:Character {name: "刘备"})-[:BLOOD_RELATION]-(family)
RETURN family
```

## Quality Assurance

### Graph Validation
- **Schema validation**: Verify graph matches schema
- **Reference integrity**: Verify all references are valid
- **Constraint validation**: Verify constraints are satisfied
- **Data consistency**: Verify data consistency

### Performance Validation
- **Query performance**: Test query response times
- **Index effectiveness**: Verify index usage
- **Memory usage**: Monitor memory consumption
- **Scalability**: Test with increasing data sizes

### Usability Validation
- **Query usability**: Test common query patterns
- **API usability**: Test API interfaces
- **Documentation**: Verify documentation completeness
- **User feedback**: Collect user feedback

## Output Format

### Graph Statistics
```json
{
  "graph_id": "unique identifier",
  "construction_date": "ISO date",
  "statistics": {
    "total_nodes": 15000,
    "total_edges": 45000,
    "node_types": {
      "Character": 5000,
      "Location": 3000,
      "Event": 4000,
      "Faction": 300
    },
    "edge_types": {
      "BLOOD_RELATION": 5000,
      "POLITICAL_RELATION": 10000,
      "MILITARY_RELATION": 15000,
      "PARTICIPATED_IN": 8000,
      "OCCURRED_AT": 4000
    }
  },
  "metrics": {
    "density": 0.003,
    "avg_clustering": 0.25,
    "avg_path_length": 4.5
  }
}
```

## Tools and Technologies
- **Graph databases**: Neo4j, Amazon Neptune, Azure Cosmos DB
- **Graph libraries**: NetworkX, igraph, Graph-tool
- **Query languages**: Cypher, Gremlin, SPARQL
- **Visualization tools**: Neo4j Bloom, Gephi, Cytoscape

## Integration Points
- Uses validated data from Skills 2-7
- Supports visualization interfaces
- Enables complex queries and analysis
- Feeds into game development

## Next Steps
After graph construction:
- Develop query interfaces
- Create visualization tools
- Enable graph analytics
- Support game scenario generation

## Notes
- Graph schema should be flexible for future extensions
- Performance optimization is critical for large graphs
- Maintain data provenance in graph properties
- Regular backups and version control for graph data
