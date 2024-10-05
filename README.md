# Telegram bot Marketing FSN



# Dev setup

TODO


# Build

```bash
docker build -t marketing-bot .
```

# Run service

```bash
docker run \
  -d \
  -e TOKEN="YOUR_BOT_TOKEN_HERE" \
  --restart="unless-stopped" \
  --name=marketing-bot \
  marketing-bot
```
