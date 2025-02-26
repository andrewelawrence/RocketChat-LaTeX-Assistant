# load_envs.py
def parse_env_file(file_path="config/.env"):
    env_vars = {}
    with open(file_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                key, val = line.split("=", 1)
                env_vars[key] = val.strip().strip('"').strip("'")
    return env_vars

if __name__ == "__main__":
    envs = parse_env_file()

    for k, v in envs.items():
        print(f'export {k}="{v}"')
