MATCH (start:Person {name: 'James Cagney'}), (end:Person {name: 'Lauren Bacall'})
CALL gds.shortestPath.dijkstra.stream({
    nodeProjection: 'Person',
    relationshipProjection: {
        KNOWS: {
            type: 'KNOWS',
            properties: 'weight'
        }
    },
    startNode: start,
    endNode: end
})
YIELD nodeId, cost
RETURN gds.util.asNode(nodeId).name AS name, cost
