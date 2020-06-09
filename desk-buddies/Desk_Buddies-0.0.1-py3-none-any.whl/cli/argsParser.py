import argparse
from datetime import datetime

from cmnSys.action import Action
from cmnUtils import dateUtils

WEEKDAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday',
            'mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun',
            'mond', 'tues', 'weds', 'thurs', 'frid', 'satd', 'sund']


def parse_args():
    parser = argparse.ArgumentParser(
        description='Communicate who can come into the office while maintaining social distancing')
    parser.add_argument("-s", "--serve", action="store_true", help="Run a DeskBuddies server [action]")
    parser.add_argument("-q", "--query", action="store_true",
                        help="Request to work (Requires date or day) [default action]")
    parser.add_argument("-r", "--remove", action="store_true",
                        help="Remove request to work (Requires date or day) [action]")
    parser.add_argument("-g", "--get", action="store_true", help="Request schedule (Requires date or day) [action]")
    parser.add_argument("-w", "--week", action="store_true", help="Request a week of schedule (get modifier)")
    parser.add_argument("-p", "--config", action="store_true", help="Update client configuration properties [action]")
    parser.add_argument("-c", "--date", type=str,
                        help="Calendar date in the form dd/mm, (format is configurable)")
    parser.add_argument("-d", "--day", type=str, help="Weekday (full or abbreviated)")
    parser.add_argument("--action", help=argparse.SUPPRESS)
    args = parser.parse_args()

    if not _parse_and_validate(args):
        return None

    return args


def _parse_and_validate(args) -> bool:
    no_date = False
    if args.day and args.date:
        return False
    elif args.day:
        try:
            args.day = WEEKDAYS.index(args.day.lower()) % 7
            args.date = dateUtils.get_next_weekday(args.day)
        except ValueError:
            print("Day not recognized.")
            return False
    elif args.date:
        try:
            # todo: make this always be in the future
            args.date = datetime.strptime(args.date, "%d/%m")
            now = datetime.now()
            args.date = datetime(now.year, args.date.month, args.date.day)
        except ValueError:
            print("Date not recognized.")
            return False
    else:
        no_date = True

    actions = ['serve', 'config', 'query', 'remove', 'get']
    args_dict = vars(args)
    num = 0
    # default action is get
    args.action = Action.QUERY
    for action in actions:
        if args_dict[action]:
            num += 1
            args.action = Action(actions.index(action))

    # should only have 1 action
    if num > 1:
        print("Multiple actions were requested. Only 1 action flag can be set.")
        return False

    if args.action > Action.CONFIG and no_date:
        print(args.action.name.lower() + " requires a day or date to be set.")
        return False

    # do any aditional parsing
    if not no_date:
        args.date = args.date.strftime("%Y%m%d")

    # there is no validation to make sure that week isn't set when other args are
    # it just won't do anything :shrug:
    return True
