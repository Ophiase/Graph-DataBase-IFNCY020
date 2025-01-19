// It's hard to find path above 110
MATCH (source)
CALL gds.dfs.stream('Graph', {
  sourceNode: source
})
YIELD path
WHERE length(path) >= 105
LIMIT 20
WITH collect(length(path)) AS pathLengths
RETURN pathLengths 
LIMIT 1