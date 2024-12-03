import asyncio

class AsyncFileWriter:
    queue = asyncio.Queue()  # Shared queue for all instances
    is_running = False  # Tracks if the writer task is running

    def __init__(self, file_path):
        self.file_path = file_path

    async def _write_to_file(self):
        """Internal method to process the queue and write to the file."""
        with open(self.file_path, 'a') as file:
            while True:
                data = await self.queue.get()
                if data is None:  # Sentinel value to stop the writer
                    break
                file.write(data + '\n')
                self.queue.task_done()

    async def writer(self, data):
        """Public method to add strings to the queue and ensure the writer is running."""
        await self.queue.put(data)

        # Start the writer task if it's not already running
        if not self.is_running:
            self.is_running = True
            asyncio.create_task(self._write_to_file())

    async def stop_writer(self):
        """Stops the writer task gracefully."""
        await self.queue.put(None)  # Add sentinel to signal the writer to stop
