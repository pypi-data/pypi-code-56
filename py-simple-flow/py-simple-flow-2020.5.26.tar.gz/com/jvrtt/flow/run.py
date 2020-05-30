import time

from com.jvrtt.flow.core.dist import apply
from com.jvrtt.flow.core.flow import BaseIngress, BaseTransformer, BaseEgress, run_flow


class Ingress(BaseIngress):

    def ingress(self, input_to_process):
        print("Ingress: Yay!! Got the input")


class Transformer(BaseTransformer):

    def transform(self, input_to_transform):
        print(f"Transform: Yay!! Got the input - {input_to_transform}")
        return input_to_transform


class Egress(BaseEgress):

    def egress(self, transform_output):
        print(f"Egress: Yay!! Got the output - {transform_output}")


def hello_world(num_of_tasks, *args, **kwargs):
    time.sleep(2)
    for _ in range(len(num_of_tasks)):
        time.sleep(1)
    print(f"Hello world - {num_of_tasks} - {args} - {kwargs}")


if __name__ == '__main__':
    start = time.time()
    apply(
        hello_world,
        list(range(10)),
        ["Pass_Arg"],
        {"key": "value"},
        num_of_buckets=10,
        bucket_size=5,
        wait_for_completion=True
    )
    end = time.time()
    print(end - start)
    run_flow(list(range(50)), Ingress(), Transformer(), Egress(), bucket_size=5, max_buckets=9)
