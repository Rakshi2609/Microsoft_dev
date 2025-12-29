# Contributing to NeuroScan AI

Thank you for your interest in contributing to NeuroScan AI! This document provides guidelines for contributing to this project.

## Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help maintain a welcoming environment

## How to Contribute

### Reporting Bugs

1. Check existing issues first
2. Use the bug report template
3. Include:
   - Clear description
   - Steps to reproduce
   - Expected vs actual behavior
   - Screenshots (if applicable)
   - Environment details

### Suggesting Enhancements

1. Check existing feature requests
2. Clearly describe the feature
3. Explain the use case
4. Consider implementation approach

### Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Make your changes
4. Add tests if applicable
5. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
6. Push to the branch (`git push origin feature/AmazingFeature`)
7. Open a Pull Request

## Development Setup

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install pytest black flake8  # Dev dependencies
```

### Frontend
```bash
cd frontend
npm install
```

## Coding Standards

### Python (Backend)
- Follow PEP 8
- Use type hints where possible
- Write docstrings for functions
- Maximum line length: 100 characters

```python
def example_function(param: str) -> dict:
    """
    Brief description of function.
    
    Args:
        param: Description of parameter
    
    Returns:
        Description of return value
    """
    pass
```

### JavaScript (Frontend)
- Use ES6+ features
- Functional components with hooks
- Use meaningful variable names
- Add comments for complex logic

```javascript
// Component example
const MyComponent = ({ prop1, prop2 }) => {
  // Component logic
  return <div>...</div>;
};
```

## Testing

### Backend Tests
```bash
cd backend
pytest tests/
```

### Frontend Tests
```bash
cd frontend
npm test
```

## Documentation

- Update README.md if adding features
- Add comments for complex algorithms
- Update API documentation
- Include examples where helpful

## Commit Messages

Follow conventional commits:

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Code style changes
- `refactor:` Code refactoring
- `test:` Adding tests
- `chore:` Maintenance tasks

Example:
```
feat: add facial landmark visualization

- Added overlay to show detected landmarks
- Implemented color coding by feature type
- Updated ResultDetails component
```

## Review Process

1. All PRs require review
2. CI checks must pass
3. Code must follow style guidelines
4. Tests must pass
5. Documentation must be updated

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.

## Questions?

Open an issue for questions or reach out to the maintainers.

Thank you for contributing! 🎉
