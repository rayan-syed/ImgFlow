import uuid

from src.broker.redis_broker import RedisBroker
from src.events.events import make_event
from src.events.topics import IMAGE_SUBMITTED


class CLI:
    def __init__(self):
        self.broker = RedisBroker()

    def print_help(self):
        print("\nAvailable Commands:")
        print("  help                 Show available commands")
        print("  upload <image_path>  Submit an image for processing")
        print("  exit                 Exit the CLI\n")

    def submit_image(self, image_path):
        image_id = f"img_{uuid.uuid4().hex[:8]}"

        event = make_event(
            IMAGE_SUBMITTED,
            {
                "image_id": image_id,
                "image_path": image_path,
                "source": "cli",
            },
        )

        self.broker.publish(IMAGE_SUBMITTED, event)

        print(f"Submitted image: {image_path}")
        print(f"Image ID: {image_id}")

    def run(self):
        print("=== ImgFlow CLI ===")
        print("type 'help' to see available commands\n")

        while True:
            try:
                raw = input(">> ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\nExiting ImgFlow CLI.")
                break

            if not raw:
                continue

            if raw == "exit":
                print("Exiting ImgFlow CLI.")
                break

            if raw == "help":
                self.print_help()
                continue

            parts = raw.split(maxsplit=1)
            command = parts[0]

            if command == "upload":
                if len(parts) < 2:
                    print("Usage: upload <image_path>")
                    continue

                image_path = parts[1]
                self.submit_image(image_path)

            else:
                print(f"Unknown command: {command}")
                print("Type 'help' to see available commands.")


if __name__ == "__main__":
    CLI().run()
