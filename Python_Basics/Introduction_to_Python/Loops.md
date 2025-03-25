# Python Loops

## 1. For Loop
Used to iterate over a sequence (list, tuple, string, range, etc.).

### Syntax:
```python
for variable in sequence:
    # Code block
```

### Example:
```python
for i in range(5):
    print(i)
```

## 2. While Loop
Repeats as long as a condition is `True`.

### Syntax:
```python
while condition:
    # Code block
```

### Example:
```python
x = 0
while x < 5:
    print(x)
    x += 1
```

## 3. Loop Control Statements
Modify loop behavior:

- **`break`**: Stops loop immediately.
- **`continue`**: Skips current iteration and moves to next.
- **`pass`**: Placeholder for future code.

### Example:
```python
for num in range(10):
    if num == 5:
        break
    print(num)
```

## 4. Nested Loops
Loops inside loops.

### Example:
```python
for i in range(3):
    for j in range(2):
        print(f"i={i}, j={j}")
```

## 5. Common Loop Applications
- Iterating over lists, tuples, and strings.
- Processing files line by line.
- Generating sequences with `range()`.
- Constructing patterns and tables.
- Implementing algorithms like Fibonacci, prime checks, etc.

