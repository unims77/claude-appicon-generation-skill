# Coding Style (General)

## Naming Conventions

Use meaningful names:

```
# Bad
d = get_data()
tmp = process(x)
flag = True

# Good
user_profile = fetch_user_profile(user_id)
formatted_report = format_monthly_report(raw_data)
is_authenticated = True
```

- Variables/functions: names that reveal intent
- Constants: no magic numbers, use named constants
- Minimize abbreviations (except conventional ones: `id`, `url`, `db`, etc.)

## Function/Method Design

Small functions, single responsibility:

- Each function does one thing only
- Functions under 50 lines
- 4 or fewer parameters (group into object/struct if exceeded)
- Minimize side effects
- Nesting 4 levels or less (use early return)

## File Organization

- 800 lines maximum per file
- High cohesion, low coupling
- Place related code close together
- One primary responsibility per file

## Error Handling

No empty catch/except blocks:

```
# Bad
try:
    process(data)
except Exception:
    pass

# Good
try:
    process(data)
except ValidationError as e:
    logger.error("Data processing failed: %s", e)
    raise ProcessingError("Input data is invalid") from e
```

- Catch specific exception types
- Include error logging
- Propagate errors appropriately
- User-friendly error messages

## Logging

Use loggers instead of print/console.log:

- Appropriate log levels (DEBUG, INFO, WARN, ERROR)
- Structured logs (include key-value pairs)
- Never log sensitive information

## DRY (Don't Repeat Yourself)

- Extract when code is duplicated 3 or more times
- But avoid over-abstraction (WET: Write Everything Twice is also acceptable)
- Separate shared logic with clear interfaces

## Code Quality Checklist

Before completing work:
- [ ] Code is readable and names are clear
- [ ] Functions are under 50 lines
- [ ] Files are under 800 lines
- [ ] Nesting is 4 levels or less
- [ ] Proper error handling is in place
- [ ] No print/console.log debugging code
- [ ] No hardcoded values
- [ ] Comments explain "why" (not "what")
