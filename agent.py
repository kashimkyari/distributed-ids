import asyncio
import aiohttp
import aiofiles
import re
import json
import logging
import yaml
from datetime import datetime

class IDSAgent:
    def __init__(self, agent_id, log_file, central_server):
        self.agent_id = agent_id
        self.log_file = log_file
        self.central_server = central_server
        self.patterns = [
            r'\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b',  # IP address
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',  # Email
            r'\b(?:https?://)?(?:[\w-]{2,}\.)+[a-zA-Z]{2,}(?:/\S*)?\b'  # URL
        ]

    async def monitor_log(self):
        async with aiofiles.open(self.log_file, mode='r') as f:
            await f.seek(0, 2)  # Move to the end of the file
            while True:
                line = await f.readline()
                if not line:
                    await asyncio.sleep(0.1)
                    continue
                await self.process_line(line)

    async def process_line(self, line):
        for pattern in self.patterns:
            if re.search(pattern, line):
                await self.send_alert(line)
                break

    async def send_alert(self, message):
        async with aiohttp.ClientSession() as session:
            alert = {
                'agent_id': self.agent_id,
                'timestamp': datetime.now().isoformat(),
                'message': message
            }
            try:
                async with session.post(f'{self.central_server}/alert', json=alert) as response:
                    if response.status != 200:
                        logging.error(f"Failed to send alert: {response.status}")
            except aiohttp.ClientError as e:
                logging.error(f"Connection error: {e}")

async def main():
    # Load configuration
    with open('agent_config.yaml', 'r') as config_file:
        config = yaml.safe_load(config_file)

    # Set up logging
    logging.basicConfig(level=logging.INFO)

    # Create and run agent
    agent = IDSAgent(config['agent_id'], config['log_file'], config['central_server'])
    await agent.monitor_log()

if __name__ == "__main__":
    asyncio.run(main())
