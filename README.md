### Koyeb
GitHub Repository linked to Koyeb Server for Distribution of CS0150 Chatbots on Rocket.Chat

#### Setup
Update .env.example variables to a .env file

#### Koyeb
Install (for Linux)
```bash
curl -fsSL https://raw.githubusercontent.com/koyeb/koyeb-cli/master/install.sh | sh
echo "add export PATH=$HOME/.koyeb/bin:$PATH to your .bashrc"
```
Login
```bash
koyeb login
```
Deployment
```bash
koyeb service redeploy operational-missie/server-name
```

#### Notes
Useful resource: https://ctan.org/tex-archive
https://developer.rocket.chat/apidocs/message


# Potential features
make the LLM tell the user's level - novice, advanced, expert, etc.?
brevity is best: use buttons, split up into multiple lines, etc.
long-term memory about the user is key.