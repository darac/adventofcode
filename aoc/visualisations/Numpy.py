import numpy as np  # noqa: N999


def boolean_array(arr: np.ndarray) -> None:
    assert len(arr.shape) == 2
    print(f" {arr.shape} ".center(arr.shape[1], "-"))
    for row in range(arr.shape[0]):
        for column in range(arr.shape[1]):
            print("#" if arr[row][column] else ".", end="")
        print()
