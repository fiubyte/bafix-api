# bafix-api

## Environments
- Prod: https://bafix-api.onrender.com/

## Usage
### Environment variables
- DB_PASSWORD

### Python
- DB_PASSWORD=<THE_PASSWORD> uvicorn app.main:app --port 80

### Docker
- docker build --tag 'bafix-api' .
- docker run -p 80:80 -e DB_PASSWORD=<THE_PASSWORD> bafix-api

## Documentation
- https://bafix-api.onrender.com/docs