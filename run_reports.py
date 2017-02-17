import os
from subscriptions import Subscriptions, Loader, Results

DATA_PATH = os.sys.argv[1]

def main():
    loader = Loader()
    subs = Subscriptions(loader)
    reports = Results(subs)
    reports.show_results(DATA_PATH)

if __name__ == '__main__':
    main()
