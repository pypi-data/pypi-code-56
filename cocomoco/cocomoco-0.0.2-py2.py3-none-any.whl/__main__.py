import sys
import argparse
try:
    import matplotlib
except:
    matplotlib = None

import cocomoco

def demo_mode():
    if not matplotlib:
        print('matplotlib required for demo-mode, please install it via pip')
        return 1

def main(args):
    if args.demo_mode:
        return demo_mode()
    if not args.sloc or args.sloc <= 0:
        print("--sloc must be larger as 0")
        return 1
    model = cocomoco.Organic()
    if args.model == 'semidetached':
         model=cocomoco.Semidetached()
    elif args.model == 'embedded':
         model=cocomoco.Embedded()
    cm = cocomoco.calculate(args.sloc, model=model)
    print('Cocomo Metric')
    print(f'Source Lines of Code: {args.sloc} (KLOC: {args.sloc // 1000})')
    print(f'Effort: {cm.effort:.1f} person-months ({cm.effort / 12.0:.1f} person-years)')
    print(f'Time to Develop: {cm.dtime:.1f} months, Staff:{cm.staff:.1f}')
    print(f'Cost: {cm.cost:.2f} with with salary of {cm.salary:.2f}')
    print(f'Used model: {cm.model_name}')
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--sloc", help="source code lines", type=int, default=None)
    parser.add_argument("--model", help="model: organic, semidetached or embedded", default='organic', choices=['organic', 'semidetached', 'embedded'],)
    parser.add_argument("--demo-mode", help="print a numpy graph", action='store_true', default=False)
    args = parser.parse_args()
    sys.exit(main(args) or 0)
