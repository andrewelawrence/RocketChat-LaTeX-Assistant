# Rocket.Chat LaTeX LLM Assistant Gateway via  Koyeb
A minimal Flask service deployed on Koyeb that connects Rocket.Chat to an early, non-distributed version of LLMProxy used in the paper [LLMProxy: Reducing Cost to Access Large Language Models](https://arxiv.org/pdf/2410.11857). Originally used to test out hosting chatbots on Rocket.Chat and has since been abandoned.

## Configuration
Place environment variables in `config/.env` (not committed) and load with the provided helper scripts.

#### Koyeb CLI quickstart (Linux):
```bash
curl -fsSL https://raw.githubusercontent.com/koyeb/koyeb-cli/master/install.sh | sh
# add export PATH=$HOME/.koyeb/bin:$PATH to your .bashrc
koyeb login
# redeploy example (replace with your service name)
koyeb service redeploy <your-org>/<your-service-name>
```

## Testing
With environment set (see `config/.env`), you can run:
```bash
./run.sh test.py
```
This script posts a test message, useful for verifying end-to-end connectivity.

## Project structure
- `app.py`: Flask app, routes (`/query`, `/show_sources`, `/upload_document`)
- `chat.py`: Welcome text and LLM response assembly
- `llmproxy.py`: Thin client for early LLMProxy (`/call`, `/retrieve`, `/add`)
- `utils.py`: AWS DynamoDB session and persistence, session ID generation, helpers
- `config/load_envs.py`: Loads `config/.env` and runs a target script
- `requirements.txt`, `Procfile`, `run.sh`

## Acknowledgements
- Early LLMProxy implementation used here is from the paper: [LLMProxy: Reducing Cost to Access Large Language Models](https://arxiv.org/pdf/2410.11857).
