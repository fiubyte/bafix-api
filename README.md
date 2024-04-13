# bafix-api

## Environments
- Prod: https://bafix-api.onrender.com/

## Usage
### Environment variables
- DB_PASSWORD
- GOOGLE_APPLICATION_CREDENTIALS
- ENV ['local'/'prod']

### Python
- GOOGLE_APPLICATION_CREDENTIALS=<GOOGLE_APPLICATION_CREDENTIALS> DB_PASSWORD=<THE_PASSWORD> uvicorn app.main:app --port 80

### Docker
- docker build --tag 'bafix-api' .
- docker run -p 80:80 -e DB_PASSWORD=<THE_PASSWORD> -e GOOGLE_APPLICATION_CREDENTIALS=<GOOGLE_APPLICATION_CREDENTIALS> bafix-api

## Documentation
- https://bafix-api.onrender.com/docs