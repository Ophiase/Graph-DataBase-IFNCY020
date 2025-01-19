MATCH (source)
CALL gds.dfs.stream('Graph', {
  sourceNode: source
})
YIELD path
WITH path
WHERE length(path) >= 2
LIMIT 1000
WITH collect(length(path)) AS pathLengths
WITH pathLengths, toFloat(size(pathLengths)) AS totalPaths
WITH reduce(s = 0.0, x IN pathLengths | s + x) AS totalLength, totalPaths
RETURN totalLength / totalPaths AS avgLength
LIMIT 1
