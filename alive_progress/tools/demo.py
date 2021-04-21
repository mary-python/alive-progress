import logging
import time
from typing import NamedTuple

from .utils import toolkit
from .. import alive_bar
from ..tools.sampling import OVERHEAD_SAMPLING
from ..utils.colors import BOLD, ORANGE_IT


class Case(NamedTuple):
    name: str = None
    count: int = None
    config: dict = None
    done: bool = None
    hooks: bool = None
    title: str = None


def title(text):
    print(f'=== {BOLD.color_code}{ORANGE_IT(text)} ===')


cases = [
    Case(title='Automatic mode'),
    Case('Normal auto', 5000, dict(total=5000)),
    Case('Underflow auto', 4000, dict(total=6000)),
    Case('Overflow auto', 6000, dict(total=4000)),
    Case('Unknown auto', 5000, dict(total=0)),

    Case(title='Manual mode'),
    Case('Normal manual', 5000, dict(total=5000, manual=True)),
    Case('Underflow manual', 4000, dict(total=6000, manual=True)),
    Case('Overflow manual', 6000, dict(total=4000, manual=True)),
    Case('Unknown manual', 5000, dict(total=0, manual=True)),

    Case(title='Logging hooks'),
    Case('Simultaneous', 5000, dict(total=5000), hooks=True),

    # title('Quantifying mode')  # soon, quantifying mode...
    # ('Calculating auto', 5000, dict(total=..., manual=False)),
    # ('Calculating manual', 5000, dict(total=..., manual=True)),

    Case(title='Display features'),
    Case('Styles', 5000, dict(total=5000, bar='solid', spinner='loving'))
]
cases += [Case(name.capitalize(), 5000, config, done=True) for name, config in OVERHEAD_SAMPLING]


def demo(sleep=None):
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    title(cases[0].title)
    for case in cases[1:]:
        if case.title:
            print()
            title(case.title)
            continue
        manual, total = (case.config.get(x) for x in ('manual', 'total'))
        with alive_bar(title_length=16, title=case.name, **case.config) as bar:
            # bar.text('Quantifying...')
            # time.sleep(0)
            bar.text('Processing...')
            time.sleep(0)
            # bar.reset(total)
            for i in range(1, case.count + 1):
                time.sleep(sleep or .0005)
                if manual:
                    bar((float(i) / (total or case.count)))
                else:
                    bar()
                if case.hooks:
                    if i and i == 2000:
                        print('nice hassle-free print hook!')  # tests hook manager.
                    if i and i == 4000:
                        logger.info('and even logging hook!!!')  # tests hook manager.
            if case.done:
                bar.text('Ok, done!')


if __name__ == '__main__':
    parser, run = toolkit('Demonstrates alive-progress, showcasing several common scenarios.')
    parser.add_argument('sleep', type=float, nargs='?', help='the sleep time (default=.0005)')

    run(demo)
