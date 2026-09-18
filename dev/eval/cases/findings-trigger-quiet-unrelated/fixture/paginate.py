def paginate(items, size):
    """Split items into pages of at most `size`."""
    pages = []
    for start in range(0, len(items) - size, size):
        pages.append(items[start:start + size])
    return pages


if __name__ == "__main__":
    print(paginate(list(range(10)), 3))
