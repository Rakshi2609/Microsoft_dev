# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability in NeuroScan AI, please report it by emailing security@neuroscan.ai (or creating a private security advisory on GitHub).

**Please do NOT create public issues for security vulnerabilities.**

### What to Include

- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

### Response Time

- We aim to acknowledge reports within 48 hours
- We will provide updates on progress
- We will notify you when the issue is fixed

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | ✅ Yes             |
| < 1.0   | ❌ No              |

## Security Measures

### Data Privacy

- No user images stored on servers
- Local processing where possible
- Minimal data retention
- Anonymous usage

### API Security

- CORS properly configured
- Input validation on all endpoints
- Rate limiting implemented
- HTTPS required in production

### Dependencies

- Regular dependency updates
- Automated vulnerability scanning
- Security patches applied promptly

### Best Practices

- Environment variables for sensitive data
- Secure credential storage
- Regular security audits
- Principle of least privilege

## Medical Data Compliance

- HIPAA compliance considerations
- GDPR compliance for EU users
- No PHI storage
- Clear data usage policies

## Responsible Disclosure

We appreciate responsible disclosure and will:

- Acknowledge your contribution
- Work with you on the fix
- Credit you in release notes (if desired)
- Provide updates on resolution

Thank you for helping keep NeuroScan AI secure!
