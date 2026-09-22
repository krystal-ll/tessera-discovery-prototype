# Simplified database for the prototype

Three tables and the connections between them. This is the whole "system" the agent reads
when it derives configuration items for the pricing step.

| Table | Columns | Rows |
|---|---|---|
| people | id, name, title, status | 6 |
| product | id, name, range, list price per case, negotiated price (Northgate), valid until | 6 |
| discount | id, name, percent, applies to, kind, since | 7 |
| connections | from, relation, to, since, note | 30 |

Relations: a person is **in charge of** products; a person **set** a discount; a discount
**applies to** products; a person **maintains price of** a product.

A configuration item is one discount row (or one price rule on the product table) together with
who set it and which products it touches. Everything is fictional.
