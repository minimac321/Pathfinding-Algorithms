
def manhattan_distance(node_a: tuple[int, int], node_b: tuple[int, int]) -> int:
    x_diff = abs(node_a[0] - node_b[0])
    y_diff = abs(node_a[1] - node_b[1])

    return x_diff + y_diff


def euclidean_distance(node_a: tuple[int, int], node_b: tuple[int, int]) -> int:
    x_diff = (node_a[0] - node_b[0])**2
    y_diff = (node_a[1] - node_b[1])**2

    return x_diff + y_diff
