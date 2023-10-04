import asyncio
import ctypes

from core.autoreger import AutoReger


def update_console_title(my_info):
    ctypes.windll.kernel32.SetConsoleTitleW(my_info)


async def main():
    print("\nMain <crypto/> moves: https://t.me/+tdC-PXRzhnczNDli\n")

    await AutoReger().start()


if __name__ == '__main__':
    update_console_title('Tea Beta Soft ☕ (@Web3Enjoyer)')
    asyncio.run(main())
