#!/bin/bash

# Update the system and install necessary dependencies
sudo apt update
sudo apt install -y make build-essential libssl-dev zlib1g-dev \
libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
libncurses5-dev libncursesw5-dev xz-utils tk-dev \
libffi-dev liblzma-dev python-openssl git

# Install pyenv
curl https://pyenv.run | bash

# Add pyenv to the shell configuration file
if [[ -f "$HOME/.bashrc" ]]; then
  echo 'export PATH="$HOME/.pyenv/bin:$PATH"' >> ~/.bashrc
  echo 'eval "$(pyenv init --path)"' >> ~/.bashrc
  echo 'eval "$(pyenv init -)"' >> ~/.bashrc
  echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bashrc
  source ~/.bashrc
elif [[ -f "$HOME/.zshrc" ]]; then
  echo 'export PATH="$HOME/.pyenv/bin:$PATH"' >> ~/.zshrc
  echo 'eval "$(pyenv init --path)"' >> ~/.zshrc
  echo 'eval "$(pyenv init -)"' >> ~/.zshrc
  echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.zshrc
  source ~/.zshrc
fi

# Install the specified Python version
PYTHON_VERSION=3.9.6
pyenv install $PYTHON_VERSION

# Create a virtual environment
ENV_NAME=Sentimental-Analysis-System
pyenv virtualenv $PYTHON_VERSION $ENV_NAME

# Activate the virtual environment
pyenv activate $ENV_NAME

# Upgrade pip
pip install pip --upgrade

# Install required Python packages
pip install -r requirements.txt

# Notify the user that the virtual environment has been created and activated
echo "Python virtual environment '$ENV_NAME' with Python $PYTHON_VERSION has been created and activated."
