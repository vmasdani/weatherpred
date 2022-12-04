#!./venv/bin/python3
import subprocess
import argparse
import yaml

parser = argparse.ArgumentParser()
parser.add_argument('action')
parser.add_argument('env')

args = parser.parse_args()

config_file = open('config.yml')
config_file_contents = config_file.read()
config_file.close()
config = yaml.safe_load(config_file_contents)

# Save template according to env
def process_template_file(input: str , output: str):
    f = open(input)
    f_contents = f.read()
    f.close()

    for c in config['env'][args.env]:
        
        f_contents = f_contents.replace(f'#{{{c}}}', f'{config["env"][args.env][c]}' )

    out = open(output, 'w+')
    out.write(f_contents)
    out.close()

process_template_file('./templates/admin.template.env', './admin/.env')
process_template_file('./templates/end_user.template.env', './end_user/.env')
process_template_file('./templates/docker-compose-template.yml', './docker-compose.yml')

if args.action == 'run':
    steps = [
        ('docker build -t weatherpred_scheduler -f Dockerfile.scheduler .', '.'),
        ('docker build -t weatherpred_backend -f Dockerfile.backend .', '.'),
        ('docker build -t weatherpred_admin_frontend -f Dockerfile.admin .', '.'),
        ('docker build -t weatherpred_end_user_frontend -f Dockerfile.end_user .', '.'),
        ('docker-compose up', '.'),
    ]

    for (c, cwd) in steps:
        subprocess.run(c, shell=True, cwd=cwd)

elif args.action == 'build':
    pass