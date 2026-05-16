# Run podman compose (optionally pass an env file path)
compose env_file=".env.local":
    podman compose --env-file {{env_file}} up