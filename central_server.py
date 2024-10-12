import asyncio
import aiohttp
from aiohttp import web
import json
import logging
import yaml
from datetime import datetime
from aio_pika import connect_robust, Message

class CentralServer:
    def __init__(self, host, port, mq_url):
        self.host = host
        self.port = port
        self.mq_url = mq_url
        self.alerts = []

    async def start(self):
        app = web.Application()
        app.router.add_post('/alert', self.handle_alert)
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, self.host, self.port)
        await site.start()
        print(f"Central server started on http://{self.host}:{self.port}")

        # Connect to RabbitMQ
        self.mq_connection = await connect_robust(self.mq_url)
        self.mq_channel = await self.mq_connection.channel()
        self.mq_queue = await self.mq_channel.declare_queue("ids_alerts")

    async def handle_alert(self, request):
        alert = await request.json()
        self.alerts.append(alert)
        print(f"Received alert: {alert}")
        await self.analyze_alert(alert)
        await self.publish_to_mq(alert)
        return web.Response(text='Alert received')

    async def analyze_alert(self, alert):
        # Implement more sophisticated analysis here
        if 'root' in alert['message'].lower():
            await self.trigger_action('Potential root access attempt detected')
        elif 'password' in alert['message'].lower():
            await self.trigger_action('Potential password attack detected')

    async def trigger_action(self, message):
        # Implement actions like sending notifications, blocking IPs, etc.
        print(f"Action triggered: {message}")

    async def publish_to_mq(self, alert):
        await self.mq_channel.default_exchange.publish(
            Message(body=json.dumps(alert).encode()),
            routing_key="ids_alerts"
        )

async def main():
    # Load configuration
    with open('server_config.yaml', 'r') as config_file:
        config = yaml.safe_load(config_file)

    # Set up logging
    logging.basicConfig(level=logging.INFO)

    # Start the central server
    server = CentralServer(config['host'], config['port'], config['mq_url'])
    await server.start()

    # Keep the server running
    while True:
        await asyncio.sleep(3600)  # Sleep for an hour

if __name__ == "__main__":
    asyncio.run(main())
