# Skill 9: Query Interface Development for Three Kingdoms Knowledge Base

## Overview
This skill covers the development of query interfaces for the Three Kingdoms knowledge base, including API endpoints, query languages, and user interfaces for accessing the knowledge graph.

## Input
- Constructed knowledge graph from Skill 8
- User requirements and use cases
- Performance requirements
- Security requirements

## Output
- REST API endpoints
- GraphQL schema (optional)
- Query language interfaces
- Web-based query interface
- Documentation and examples

## Query Interface Types

### 1. REST API
- **Entity queries**: Query for entities by type, attributes
- **Relationship queries**: Query for relationships between entities
- **Event queries**: Query for events by time, location, participants
- **Complex queries**: Multi-entity, multi-relationship queries

### 2. GraphQL Interface
- **Schema definition**: Define GraphQL schema for knowledge graph
- **Query language**: Enable complex GraphQL queries
- **Type safety**: Ensure type-safe queries
- **Introspection**: Enable schema introspection

### 3. Natural Language Interface
- **Natural language queries**: Query using natural language
- **Intent recognition**: Recognize user query intent
- **Query translation**: Translate natural language to graph queries
- **Result formatting**: Format results for natural language presentation

### 4. Web Interface
- **Search interface**: Web-based search functionality
- **Visual query builder**: Drag-and-drop query construction
- **Result visualization**: Visual presentation of results
- **Export functionality**: Export query results

## API Endpoint Design

### Entity Endpoints
```python
# Get entity by ID
GET /api/entities/{entity_id}
Response: Entity details with relationships

# Search entities
GET /api/entities?type=character&name=刘备
Response: List of matching entities

# Get entity relationships
GET /api/entities/{entity_id}/relationships
Response: All relationships for the entity

# Get entity neighbors
GET /api/entities/{entity_id}/neighbors?depth=2
Response: Neighboring entities within specified depth
```

### Event Endpoints
```python
# Get event by ID
GET /api/events/{event_id}
Response: Event details with participants and location

# Search events by time range
GET /api/events?start_year=200&end_year=210
Response: Events in time range

# Search events by location
GET /api/events?location=赤壁
Response: Events at location

# Get event chain
GET /api/events/{event_id}/chain?type=causal
Response: Causal chain of events
```

### Relationship Endpoints
```python
# Get relationship by ID
GET /api/relationships/{relationship_id}
Response: Relationship details

# Query relationships between entities
GET /api/relationships?source={source_id}&target={target_id}
Response: Relationships between entities

# Get relationship network
GET /api/relationships/network?center={entity_id}&depth=2
Response: Relationship network around entity

# Get shortest path
GET /api/relationships/path?source={source_id}&target={target_id}
Response: Shortest path between entities
```

### Complex Query Endpoints
```python
# Execute complex query
POST /api/queries
Body: Query specification
Response: Query results

# Get character profile
GET /api/profiles/characters/{character_name}
Response: Complete character profile

# Get faction overview
GET /api/profiles/factions/{faction_name}
Response: Complete faction overview

# Get timeline
GET /api/timelines?character={character_name}&type=life
Response: Character life timeline
```

## Query Language Design

### Simple Query Language
```
# Basic entity query
FIND character WHERE name = "刘备"

# Relationship query
FIND relationships BETWEEN "刘备" AND "曹操"

# Event query
FIND events WHERE year = 208 AND location = "赤壁"

# Complex query
FIND path FROM "刘备" TO "曹操" MAX_DEPTH 3
```

### Advanced Query Features
- **Pattern matching**: Match complex graph patterns
- **Temporal filtering**: Filter by time ranges
- **Spatial filtering**: Filter by geographic regions
- **Aggregation**: Aggregate and summarize results
- **Sorting**: Sort results by various criteria
- **Pagination**: Paginate large result sets

## Natural Language Query Processing

### Intent Recognition
- **Entity lookup**: "Who is Liu Bei?"
- **Relationship query**: "What is the relationship between Liu Bei and Guan Yu?"
- **Event query**: "What happened at Red Cliffs?"
- **Temporal query**: "What did Zhuge Liang do in 234 AD?"
- **Comparative query**: "Who is smarter, Zhuge Liang or Sima Yi?"

### Query Translation
```python
class NaturalLanguageQueryTranslator:
    def translate_query(self, natural_query):
        # Extract entities
        entities = self.extract_entities(natural_query)
        
        # Identify intent
        intent = self.identify_intent(natural_query)
        
        # Extract constraints
        constraints = self.extract_constraints(natural_query)
        
        # Generate graph query
        graph_query = self.generate_graph_query(intent, entities, constraints)
        
        return graph_query
```

### Result Formatting
- **Natural language generation**: Convert results to natural language
- **Contextual explanation**: Provide context for results
- **Source attribution**: Include source information
- **Confidence indicators**: Show confidence in results

## Web Interface Design

### Search Interface
- **Simple search**: Basic search box with filters
- **Advanced search**: Complex search with multiple criteria
- **Autocomplete**: Suggest entities as user types
- **Search history**: Maintain search history

### Visual Query Builder
- **Drag-and-drop**: Drag entities to build queries
- **Visual relationships**: Show relationships visually
- **Query preview**: Preview query before execution
- **Save queries**: Save and reuse queries

### Result Visualization
- **Entity cards**: Display entity information in cards
- **Network graphs**: Show relationship networks
- **Timelines**: Display temporal information
- **Maps**: Display geographic information

### Export Functionality
- **JSON export**: Export results as JSON
- **CSV export**: Export results as CSV
- **Graph export**: Export subgraphs
- **Report generation**: Generate formatted reports

## Performance Optimization

### Query Optimization
- **Index utilization**: Ensure queries use indexes
- **Query caching**: Cache frequent queries
- **Query planning**: Optimize query execution plans
- **Result pagination**: Paginate large result sets

### Caching Strategy
- **Entity cache**: Cache frequently accessed entities
- **Query cache**: Cache query results
- **Session cache**: Cache user session data
- **CDN caching**: Cache static content

### Load Balancing
- **Read replicas**: Distribute read queries
- **Connection pooling**: Manage database connections
- **Rate limiting**: Limit query rates
- **Query queuing**: Queue heavy queries

## Security Considerations

### Authentication
- **API keys**: API key authentication
- **OAuth**: OAuth integration
- **Session management**: Secure session handling
- **Token refresh**: Token refresh mechanism

### Authorization
- **Role-based access**: Role-based access control
- **Resource-based access**: Resource-level permissions
- **Query restrictions**: Restrict complex queries
- **Rate limiting**: Prevent abuse

### Data Protection
- **Input validation**: Validate all inputs
- **SQL injection prevention**: Prevent injection attacks
- **Data encryption**: Encrypt sensitive data
- **Audit logging**: Log all queries

## Documentation

### API Documentation
- **Endpoint reference**: Complete endpoint documentation
- **Request/response formats**: Detailed format specifications
- **Error codes**: Error code reference
- **Examples**: Usage examples

### User Documentation
- **Getting started**: Quick start guide
- **Query guide**: Query writing guide
- **Best practices**: Best practice recommendations
- **FAQ**: Frequently asked questions

### Developer Documentation
- **Architecture documentation**: System architecture
- **Integration guide**: Integration instructions
- **Extension guide**: How to extend the system
- **Troubleshooting**: Common issues and solutions

## Output Format

### API Response Example
```json
{
  "status": "success",
  "data": {
    "entity": {
      "entity_id": "character_liubei",
      "name": "刘备",
      "type": "character",
      "attributes": {
        "style_name": "玄德",
        "faction": "蜀",
        "birth_year": 161,
        "death_year": 223
      },
      "relationships": [
        {
          "type": "BLOOD_RELATION",
          "target": "character_liushan",
          "properties": {"relation": "father"}
        }
      ]
    }
  },
  "metadata": {
    "query_time": "0.05s",
    "source": "knowledge_graph",
    "confidence": 0.95
  }
}
```

## Tools and Technologies
- **Web frameworks**: FastAPI, Flask, Django
- **API documentation**: Swagger/OpenAPI
- **GraphQL**: Apollo, Graphene
- **Natural language processing**: spaCy, transformers
- **Frontend frameworks**: React, Vue.js

## Integration Points
- Uses knowledge graph from Skill 8
- Supports web interface development
- Enables mobile app development
- Facilitates third-party integrations

## Next Steps
After query interface development:
- Develop web-based visualization
- Create mobile applications
- Enable third-party integrations
- Collect user feedback

## Notes
- API design should be intuitive and consistent
- Performance is critical for user experience
- Security should be built in from the start
- Documentation should be comprehensive and up-to-date
