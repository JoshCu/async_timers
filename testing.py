import asyncio
import datetime

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

timeout = 15


def print_progress_bar(
        iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█', printEnd="\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=printEnd)
    # Print New Line on Complete
    if iteration == total:
        print()


async def timer():
    now = datetime.datetime.now()
    timeout_microseconds = timeout*1000
    for i in range(timeout_microseconds):
        time_passed = (datetime.datetime.now() - now).total_seconds() * 1000
        print_progress_bar(time_passed, timeout_microseconds,
                           prefix='Progress:', suffix='Timer', length=50)
        await asyncio.sleep(.1)
    return True


async def run():
    # run the timer while the program is running
    await asyncio.sleep(5)
    return True
    # end the timer when the program is done


async def command_with_timer():
    tasks = [timer(), run()]
    while tasks:
        finished, unfinished = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)

        for x in finished:
            result = x.result()

            if result:
                # cancel the other tasks, we have a result. We need to wait for the cancellations
                # to propagate.
                for task in unfinished:
                    task.cancel()
                await asyncio.wait(unfinished)

                return

        tasks = unfinished


def run_commands():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(command_with_timer())


for i in range(100):
    print_progress_bar(i, 99, prefix='Progress:', suffix='Complete', length=50)
    print()
    run_commands()
    # clear the line and move cursor up
    LINE_UP = '\033[1A'
    LINE_CLEAR = '\x1b[2K'
    print(LINE_CLEAR, end=LINE_UP)
