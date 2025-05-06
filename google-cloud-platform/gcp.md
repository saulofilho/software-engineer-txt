Esses serviços são frequentemente combinados em arquiteturas modernas. Por exemplo:

Arquivos chegam no Cloud Storage → um evento dispara uma Cloud Function → que publica algo no Pub/Sub → processado por outro serviço que grava dados no BigQuery → com alguma lógica mais pesada rodando em uma Compute Engine.
