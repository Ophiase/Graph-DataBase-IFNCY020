MATCH (w:Work)
RETURN avg(w.runtime_minutes) AS average_runtime
