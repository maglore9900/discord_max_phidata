import asyncio
from modules import write_handler

async def main():
    w = write_handler.AsyncFileWriter("output.txt")

    # Add multiple items to the queue
    for i in range(6):
        w.writer(f"this is test {i}")

    # Allow some time for the writer to process
    await asyncio.sleep(1)

    # Stop the writer gracefully
    await w.stop_writer()

# Run the main function
asyncio.run(main())
