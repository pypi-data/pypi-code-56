import synacell.cmodule


def test_1() -> (int, str):
    """
    Test creating net in the memory space of the snn.dll

    :return: (int, str) 0 is success, everything else is error, str is mesage
    """
    snn = synacell.cmodule.Snn()

    print(f"Net count = {snn.net_count()}")
    snn.create_net()
    print(f"Net count = {snn.net_count()}")

    if snn.net_count() == 1:
        return 0, "Success"
    else:
        return 1, f"Net count is {snn.net_count()}"


def run_all():
    val, msg = test_1()
    if val == 0:
        print("All tests passed!")
    else:
        print(f"Test {1} failed with error message: {msg}")


if __name__ == '__main__':
    '''
    1. If the module is ran (not imported) the interpreter sets this at the top of your module:
    ```
    __name__ = "__main__"
    ```
    2. If the module is imported: 
    ```
    import rk
    ```
    The interpreter sets this at the top of your module:
    ```
    __name__ = "rk"
    ```
    '''
    run_all()