// Problem: the graph is directed
// Double BFS doesn't is suited for directed graph.
// - We either need to modify BFS to ignore the direction (java)
// - Or we could complte the graph (long)

MATCH (source)
CALL gds.dfs.stream('Graph', {
  sourceNode: source
  })
  YIELD path
  WHERE length(path) >= 105
  LIMIT 1
  
  WITH head(nodes(path)) AS firstNode
  
  CALL gds.bfs.stream(
  'Graph', { sourceNode: firstNode }
  )
  YIELD path
  LIMIT 1
  
  WITH tail(nodes(path))[0] AS secondNode
  
  CALL gds.bfs.stream(
  'Graph', { sourceNode: secondNode }
  )
  YIELD path
  
  RETURN length(path)
