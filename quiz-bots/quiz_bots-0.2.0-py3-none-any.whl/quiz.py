import glob
import re
from typing import List, Tuple


def fetch_quiz_content_from_file(filepath: str) -> List[Tuple[str, str]]:
    """Fetch quiz question and answer from file."""
    with open(filepath, 'r', encoding='KOI8-R') as file_with_quiz_content:
        raw_quiz_content = iter(file_with_quiz_content.read().split('\n\n'))

    return [
        (
            re.sub(r'Вопрос \d+:\n', '', text_block),
            re.sub(r'Ответ:\n', '', next(raw_quiz_content)),
        )
        for text_block in raw_quiz_content
        if text_block.startswith('Вопрос')
    ]


def send_quiz_content_to_redis(args, redis_client) -> None:
    """Sends quiz content to Redis."""
    file_paths = list(glob.glob(f'{args.quiz_questions_folder_path}/**/*.txt', recursive=True))
    for file_path in file_paths:
        for question, answer in fetch_quiz_content_from_file(file_path):
            redis_client.hset('Questions', question, answer)
