import argparse

import redis

from quiz_bots.quiz import send_quiz_content_to_redis
from quiz_bots.settings import db_endpoint, db_password
from quiz_bots.tg_bot import start_tg_bot
from quiz_bots.vk_bot import start_vk_bot


def get_redis_client() -> redis.client.StrictRedis:
    """Connect to Redis."""
    redis_host, redis_port = db_endpoint.split(':')
    redis_password = db_password
    return redis.StrictRedis(
        host=redis_host,
        port=redis_port,
        password=redis_password,
        charset='utf-8',
        decode_responses=True,
    )


def create_parsers() -> argparse.ArgumentParser:
    """Create parsers of cli arguments."""
    parser = argparse.ArgumentParser(description='User database utility')

    subparsers = parser.add_subparsers()
    parser_start_tg_bot = subparsers.add_parser('tg-bot', help='Start tg bot')
    parser_start_tg_bot.set_defaults(func=start_tg_bot)
    parser_start_vk_bot = subparsers.add_parser('vk-bot', help='Start vk bot')
    parser_start_vk_bot.set_defaults(func=start_vk_bot)

    parser_export_quiz_content = subparsers.add_parser(
        'export_quiz_content',
        help='Export quiz content to Redis',
    )
    parser_export_quiz_content.add_argument(
        'quiz_questions_folder_path',
        help='Quiz questions folder path',
    )
    parser_export_quiz_content.set_defaults(func=send_quiz_content_to_redis)
    return parser


def main() -> None:
    """Entry point."""
    args = create_parsers().parse_args()
    redis_client = get_redis_client()
    args.func(args, redis_client)


if __name__ == '__main__':
    main()
