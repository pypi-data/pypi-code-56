import funcy
import tqdm

from download_accelerator import constants


def write_to_file(output: str, content: bytes, name: str, position: int = 0) -> None:
    with open(output, "wb") as file:
        chunks = funcy.chunks(1024, content)
        with tqdm.tqdm(desc=constants.SAVING_FILE_PROGRESS_BAR.format(name=name, output=output),
                       total=len(content), unit=constants.SAVING_FILE_PROGRESS_UNIT, unit_scale=True, unit_divisor=1024,
                       position=position) as bar:
            for chunk in chunks:
                bar.update(len(chunk))
                file.write(chunk)
