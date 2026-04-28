import numpy as np  # noqa: N999

TWO_D_ARRAY_LEN = 2


def boolean_array(arr: np.ndarray) -> None:
    assert len(arr.shape) == TWO_D_ARRAY_LEN
    print(f" {arr.shape} ".center(arr.shape[1], "-"))
    for row in range(arr.shape[0]):
        for column in range(arr.shape[1]):
            print("#" if arr[row][column] else ".", end="")
        print()
