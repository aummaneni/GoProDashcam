import argparse
import asyncio
import logging
from typing import Optional

from rich.console import Console

from open_gopro import WirelessGoPro
from open_gopro.logger import set_stream_logging_level, setup_logging
from open_gopro.util import add_cli_args_and_parse, ainput

console = Console()

def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Connect to a GoPro camera's Wifi Access Point.")
    return add_cli_args_and_parse(parser)


async def main(args: argparse.Namespace) -> None:
    setup_logging(__name__, args.log)
    gopro: Optional[WirelessGoPro] = None

    async with WirelessGoPro(args.identifier, wifi_interface=args.wifi_interface, sudo_password=args.password) as gopro:
        # Now we only want errors
        set_stream_logging_level(logging.ERROR)
        await ainput("[green]Press enter to disconnect Wifi and exit...", console.print)
        console.print("Exiting..")

    if gopro:
        await gopro.close()

def entrypoint() -> None:
    asyncio.run(main(parse_arguments()))

if __name__ == "__main__":
    entrypoint()
