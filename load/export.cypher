// to cypher
CALL apoc.export.cypher.all('export.cypher', {format: 'cypher-shell'})

// to csv
CALL gds.graph.export.csv('my-graph', {
  exportName: 'my-export',
  nodePropertyWhitelist: ['*'],
  relationshipPropertyWhitelist: ['*']
})

// to JSON
CALL apoc.export.json.all('export.json', {useTypes:true})
