import os

# Get all environment variables
env_vars = os.environ

# Print all environment variables
for key, value in env_vars.items():
    print(f'{key}: {value}')