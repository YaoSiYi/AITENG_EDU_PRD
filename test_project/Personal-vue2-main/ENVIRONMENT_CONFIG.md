# Environment Configuration Guide

## Overview

This project supports multiple environments:
- Development (`.env.development`)
- Staging (`.env.staging`)
- Production (`.env.production`)

Each environment file contains key-value pairs that are injected into the application at build time.

## Environment Variables

### Core Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `ENV` | Environment identifier | development/staging/production |
| `NODE_ENV` | Node environment | development/production |
| `VUE_APP_BASE_API` | Base API URL | https://api.example.com |
| `VUE_APP_UPLOAD_URL_TEST` | Test upload URL | https://test-api.example.com |
| `VUE_APP_UPLOAD_URL_PROD` | Production upload URL | https://api.example.com |

### Adding New Environment Variables

1. Prefix all custom environment variables with `VUE_APP_`
2. Add the variable to all environment files
3. Document the variable in this guide
4. Access in code using `process.env.VUE_APP_VARIABLE_NAME`

### Environment-Specific Configuration

#### Development
```
ENV = 'development'
NODE_ENV = 'development'
VUE_APP_BASE_API = 'http://localhost:8001'
VUE_APP_UPLOAD_URL_TEST = 'http://localhost:8001'
VUE_APP_DEBUG = 'true'
```

#### Staging
```
ENV = 'staging'
NODE_ENV = 'production'
VUE_APP_BASE_API = 'https://staging-api.example.com'
VUE_APP_UPLOAD_URL_TEST = 'https://staging-api.example.com'
VUE_APP_DEBUG = 'false'
```

#### Production
```
ENV = 'production'
NODE_ENV = 'production'
VUE_APP_BASE_API = 'https://api.example.com'
VUE_APP_UPLOAD_URL_PROD = 'https://api.example.com'
VUE_APP_DEBUG = 'false'
```

## Usage in Code

Access environment variables in your Vue components or JavaScript files:

```javascript
const apiUrl = process.env.VUE_APP_BASE_API
const isDebug = process.env.VUE_APP_DEBUG === 'true'
```

## Best Practices

1. Never store sensitive information like passwords or private keys in environment files
2. Always document new environment variables
3. Keep environment files in sync across all environments
4. Use descriptive names for variables
5. Group related variables together
6. Add comments to explain complex configurations

## Custom Environment Files

You can create additional environment files following the naming convention:
- `.env.[mode]`
- `.env.[mode].local`

For example:
- `.env.testing`
- `.env.testing.local`

To use a custom environment:
```bash
npm run build --mode testing
```

## Local Overrides

Local environment files (`.env.*.local`) are not committed to version control and can be used for:
- Developer-specific settings
- Machine-specific configurations
- Temporary overrides

## Security Considerations

1. Environment variables are embedded in the client-side bundle
2. Do not store secrets or private keys
3. Use server-side environment variables for sensitive data
4. Review all environment variables before deployment