import json
import sys
from pathlib import Path

from dephell.commands import DepsOutdatedCommand
from dephell.config import Config
from dephell.venvs import VEnv


def test_deps_outdated_command_file(temp_path: Path, capsys):
    reqs_path = temp_path / 'requirements.txt'
    reqs_path.write_text('six==1.11.0')

    config = Config()
    config.attach({
        'to': dict(format='piplock', path=str(reqs_path)),
        'level': 'WARNING',
        'silent': True,
    })

    command = DepsOutdatedCommand(argv=[], config=config)
    result = command()

    captured = capsys.readouterr()
    output = json.loads(captured.out)
    assert result is True
    assert len(output) == 1
    assert output[0]['name'] == 'six'
    assert output[0]['installed'] == ['1.11.0']
    assert output[0]['latest'] != '1.11.0'


def test_deps_outdated_command_venv(temp_path: Path, capsys):
    venv_path = temp_path / 'venv'
    venv = VEnv(path=venv_path)
    assert venv.exists() is False
    venv.create(python_path=sys.executable)

    config = Config()
    config.attach({
        'project': str(temp_path),
        'venv': str(venv_path),
        'level': 'WARNING',
        'silent': True,
    })

    command = DepsOutdatedCommand(argv=[], config=config)
    result = command()

    captured = capsys.readouterr()
    output = json.loads(captured.out)
    assert result is True
    names = {line['name'] for line in output}
    assert len(names - {'pip', 'setuptools'}) == 0
