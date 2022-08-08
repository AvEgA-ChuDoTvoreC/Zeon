
# Kraken

[![Kraken](pic/kraken.svg)]()

[![Bash](pic/bash.svg)](https://www.gnu.org/software/bash/)
[![Python](pic/python.svg)](https://python.org/downloads/release/python-350/)
[![Ansible](pic/ansible.svg)](https://docs.ansible.com/ansible/latest/)
[![Jinja](pic/jinja.svg)](https://jinja.palletsprojects.com/en/3.1.x/kali)

[![Kali](pic/kali.svg)](https://www.kali.org/)
[![Debian](pic/debian.svg)](https://www.debian.org/)

<b>Kraken</b> - multi functional software which build <b>DEBAIN packages</b>, sign them at Node
with <b>OS AstraLinux Special Edition</b> via <b>Closed Software Environment</b> or <b>Digital Signature (GPG)</b>.
Generate <b>ISO image</b> based on built <b>APT repository</b> for future deploy via <b>Ansible</b>.

<br />

## Content

* [Installation from Source](#installation-from-source)
* [Kraken Workspace](#kraken-workspace)
* [Kraken project File Structure](#kraken-project-file-structure)
* [Kraken Extra Info](#kraken-extra-info)
    * [Setup Virtual Environment](#setup-virtual-environment)
    * [Ansible commands](#ansible-commands)
    * [PIP commands](#pip-commands)
    * [README file syntax](#readme-file-syntax)
* [The End](#the-end)

<br />

## Installation from Source

Clone the repo.
```bash
$ git clone http://bitbucket.01050-1.ru/projects/kraken.git
$ cd kraken/usr/bin
```

Create ```.env``` file in Kraken project root directory with fields:
```.dotenv
KRAKEN_DEBUG=True
```

Exec next commands:
```bash
$ ./kraken setup-from-source
```

Collect built Kraken package ```kraken_x.x.x-x_amd64.deb``` and install it via ```apt```.
```bash
$ cd ${HOME}/.kraken/artifacts
$ sudo apt install ./kraken_<version>_amd64.deb
```

Read manual page to get know how to deal with Kraken:

```bash
$ man kraken
$ man -L ru kraken       # Russian version supported
```

<br />

## Kraken Workspace

Kraken uses next directories to build & deploy projects:
```
$HOME/.kraken
    .
    ├── artifacts                      - здесь храняться результаты сборок
    │   ├── daei_467379_005_02.iso
    │   └── kraken_1.0.0-4_amd64.deb
    ├── build                          - рабочая директория сборки проектов
    │   ├── CD/                        - директория сборки ISO
    │   └── project_name/              - директория сборки DEBIAN пакета
    └── keys                           - здесь храняться GPG ключи Пользователя и Предприятия
        ├── agat.fpr
        ├── agat-gpg-keys.tar.gz
        ├── user.fpr
        └── user-gpg-keys.tar.gz

```

<br />

## Kraken project File Structure

Kraken source directories explanations:
```
../KRAKEN
    .
    ├── deploy                  - папка ansible ролей для деплоя
    │   ├── README.md
    │   ├── ansible.cfg
    │   ├── deploy_playbook.yml       - файл ansible ролей, которые будут исполненны на удалленных нодах
    │   ├── vault_vars.yml            - файл переменных ansible хранилища
    │   └── roles/              - папка ролей для deploy_playbook.yml, для каждой роли свои tasks
    ├── kraken
    │   ├── doc/                - папка мануалов ($ man kraken && man -L ru kraken)
    │   ├── etc                 - папка конфигурационных файлов
    │   │   ├── kraken
    │   │   │   ├── debsign.conf      - конфиг ноды для подключения и подписи в замкнутой среде разработки Astra Linux
    │   │   │   ├── hosts.conf        - конфиг ansible хостов (ноды, на которые будут ставиться проекты)
    │   │   │   ├── kraken_base.conf  - конфиг базовой настройки kraken
    │   │   │   ├── kraken.conf       - конфиг проекта (если kraken не найдет kraken.conf в проекте пользователя, будет использован конфиг по умолчанию)
    │   │   │   ├── org.conf          - конфиг для генерации GPG ключей Агата
    │   │   │   ├── user.conf         - конфиг для генерации GPG ключей Разработчика
    │   │   │   └── ssh.conf          - конфиг для генерации SSH ключей для подключения к удаленным нодам
    │   │   └── skel/
    │   ├── opt/                - пустая папка
    │   ├── usr/                - папка исполняемого бинарного файла kraken
    │   └── var/                - папка скриптов и библиотек
    ├── .env
    ├── .gitignore
    ├── README.md
    ├── requirements.txt
    └── venv/
```
<br />

## Kraken Extra Info

<br />

#### Setup Virtual Environment

Download [pipenv](https://docs.pipenv.org/):
```bash
$ pip install pipenv
```

Setup project virtual environment:
```bash
$ pipenv install --dev
$ pipenv shell
```
<br />

#### Ansible commands

Check this out:
```bash
$ ansible-galaxy init <role>
$ ansible --module-name ping --inventory=./hosts.conf <host> 
$ ansible-playbook --inventory=./hosts.conf playbook.yml
```

<br />

#### PIP commands

Check this out:
```bash
$ twine upload --verbose --repository-url http://localhost:8000/ ${HOME}/pip-packages/<package>/*
$ dir2pi ${HOME}/pip-packages/packages/ -S
$ pip2pi http://localhost:8000:${HOME}/pip-packages/<package>/ <package>
$ pip download --no-cache-dir --no-binary :all: <package>
$ pip download --no-cache-dir <package>
$ pip install --no-cache-dir <package> 
$ pip uninstall -y $(pip show <package> | grep Requires | sed 's/Requires: //g; s/,//g') <package>
```

<br />

#### APT commands

Check this out:
```bash
sudo apt install \
         --reinstall \
         -d \
         -o dir::cache=$(pwd)/<packages_folder> \
         <packages>

sudo apt install \
         --reinstall \
         -d \
         -o dir::cache=$(pwd)/<packages_folder> \
         $(apt-cache depends \
                     --recurse \
                     --no-recommends \
                     --no-suggests \
                     --no-conflicts \
                     --no-breaks \
                     --no-replaces \
                     --no-enhances \
                     <packages> | grep "^\w" | sort -u)
```

<br />

#### README file Syntax

To set header height use next syntax:
```
# <Big header>
## <Medium header>
### <Small header>
```

Use package ```tree``` to list folder structure.
```bash
$ sudo apt install tree
$ tree -L 2
```

Linked content in ```README.md```.
```
* [Header](#Hashtag-to-header)
* [Kraken workspace](#kraken-workspace)
```

Download badge from [shields.io](https://img.shields.io/badge/).
```bash
$ wget 'https://img.shields.io/badge/ansible-v2.12.3-blue?logo=ansible' -O ansible.svg
```

Insert badge with relative path.
```bash
![pic-3](./pic/ansible.svg)
```

Use checkboxes.
```bash
- [x] Write tests
- [ ] GitHub CI/CD build
```

Use tabs between headers.
```
<br />
```

Mark your code with ```python```, ```bash```, etc.
```
class Bar:
    __doc__ = "Class Bar with method foo"
    
    def __init__(self):
        pass
    
    def foo(self, *args, **kwargs) -> None:
        pass
```

```bash
$ declare -gx GLOBAL_R_ARG=1 
$ echo $(ls -lah | grep "python")
```

```bash
SELECT * FROM fcs_user;

.headers on
.mode column
```

<br />

### The End