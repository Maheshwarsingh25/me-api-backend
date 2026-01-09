# MongoDB Schema

## Database: me_api

### Collection: profile
{
  "name": "string",
  "email": "string",
  "education": "string",
  "skills": ["string"],
  "projects": [
    {
      "title": "string",
      "description": "string",
      "links": ["string"]
    }
  ],
  "work": [
    {
      "company": "string",
      "role": "string",
      "duration": "string"
    }
  ],
  "links": {
    "github": "string",
    "linkedin": "string",
    "portfolio": "string"
  }
}
