from portfolio import portfolio as pf
import argparse


def arguments():
    parser = argparse.ArgumentParser(description='Check-Access Reporting.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--myportfolio", help="Portfolio details",
                        action='store_true')
    parser.add_argument("--special", help="Portfolio details",
                        default=None)

    return parser


def main():
    parser = arguments()
    args = parser.parse_args()
    if args.myportfolio:
        pf.Portfolio().portfolio_summary()
    if args.special:
        pf.Portfolio().portfolio_summary(args.special)


if __name__ == "__main__":
    main()
