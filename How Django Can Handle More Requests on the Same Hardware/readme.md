## How Django Can Handle More Requests on the Same Hardware

| Optimization Technique | Typical Gain | Why it Works |
|-----------------------|--------------|--------------|
| Proper database indexing | 2× – 10× | Removes full table scans |
| Query optimization (avoid N+1) | 2× – 5× | Cuts DB round-trips drastically |
| Optimizing ORM joins (`select_related`, `prefetch_related`) | 1.5× – 3× | Fewer queries per request |
| Reducing query payload (`only`, `values`) | 1.2× – 2× | Less CPU + memory per query |
| Pagination instead of full lists | 3× – 20× | Avoids loading massive datasets |
| Database connection pooling | 1.5× – 3× | Removes connection setup cost |
| Redis / in-memory caching | 5× – 50× | DB bypass for hot data |
| HTTP response caching | 10× – 100× | Full request bypass |
| Serving static files via Nginx | 1.5× – 2× | Django freed from I/O |
| Gzip / Brotli compression | 1.2× – 1.5× | Faster responses, less bandwidth |
| CDN for static & media | 2× – 5× | Requests never reach server |
| Async views (external APIs) | 2× – 4× | Threads not blocked |
| Avoiding blocking I/O | 2× – 5× | Workers stay free |
| Gunicorn worker & thread tuning | 1.5× – 3× | Better CPU utilization |
| Rate limiting abusive requests | Indirect but critical | Protects real users |
