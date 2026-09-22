# Simplified database for the prototype

Three tables and the connections between them. This is the whole "system" the agent reads
when it derives configuration items for the pricing step.

| Table | Columns | Rows |
|---|---|---|
| people | id, name, title, status | 4 |
| product | id, name, range, list price per case | 4 |
| discount | id, name, percent, applies to, since | 5 |
| connections | from, relation, to, since, note | 18 |

Relations: a person is **in charge of** products; a person **set** a discount; a discount
**applies to** products.

A configuration item is one pricing rule (one or two discount rows) together with who set it and
which products it touches. Three items for the prototype. Everything is fictional.
