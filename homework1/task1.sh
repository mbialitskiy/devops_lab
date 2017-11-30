#!/bin/bash

#curl -L https://raw.github.com/yyuu/pyenv-installer/master/bin/pyenv-installer | bash
git clone https://github.com/pyenv/pyenv.git ~/.pyenv
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bash_profile
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bash_profile
echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n  eval "$(pyenv init -)"\nfi' >> ~/.bash_profile
export PATH="/home/student/.pyenv/bin:$PATH" >> ~/.bash_profile
exec "$SHELL"
yum install -y zlib-devel bzip2 bzip2-devel readline-devel sqlite sqlite-devel openssl-devel xz xz-devel
pyenv install 3.5.4
pyenv install 2.7.14

pyenv virtualenv 2.7.14 virtenv1
pyenv virtualenv 3.5.4 virtenv2









