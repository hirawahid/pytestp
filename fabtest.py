import configparser
import time
from io import StringIO

from fabric.api import run
from fabric.context_managers import settings, hide
from fabric.operations import sudo, get
from fabric.state import env

config = configparser.ConfigParser()
config.read('settings.ini')
env.user = config['fabric']['user']
env.password = config['fabric']['pwd']
env.hosts = config['fabric']['hosts']
env.REPLY = 'Y'


def start_config():
    run("echo y|start-config")

def nof():
    return run("ls /data/afiniti/log_tables | wc -l")

def download_agent_batch():
    acdr_file=run("ls -t /data/afiniti/log_tables| grep -i agent_batch | head -1")
    get('/data/afiniti/log_tables/'+acdr_file,'C:/Users/Hira.Wahid/PycharmProjects/pytestp/downloads')
    return acdr_file

def download_call_batch():
    acdr_file=run("ls -t /data/afiniti/log_tables| grep -i call_batch | head -1")
    get('/data/afiniti/log_tables/'+acdr_file,'C:/Users/Hira.Wahid/PycharmProjects/pytestp/downloads')
    return acdr_file

def download_instance_batch():
    acdr_file=run("ls -t /data/afiniti/log_tables| grep -i instance_batch | head -1")
    get('/data/afiniti/log_tables/'+acdr_file,'C:/Users/Hira.Wahid/PycharmProjects/pytestp/downloads')
    return acdr_file

def download_eval_summary():
    acdr_file=run("ls -t /data/afiniti/log_tables| grep -i eval_summary | head -1")
    get('/data/afiniti/log_tables/'+acdr_file,'C:/Users/Hira.Wahid/PycharmProjects/pytestp/downloads')
    return acdr_file

def download_eval_logs():
    acdr_file=run("ls -t /data/afiniti/log_tables| grep -i eval_logs | head -1")
    get('/data/afiniti/log_tables/'+acdr_file,'C:/Users/Hira.Wahid/PycharmProjects/pytestp/downloads')
    return acdr_file

def download_acdr():
    acdr_file=run("ls -t /data/afiniti/log_tables| grep -i t_acdr | head -1")
    get('/data/afiniti/log_tables/'+acdr_file,'C:/Users/Hira.Wahid/PycharmProjects/pytestp/downloads')
    return acdr_file

def download_aglog():
    aglog_file = run("ls -t /data/afiniti/log_tables| grep -i t_aglog | head -1")
    get('/data/afiniti/log_tables/' + aglog_file, 'C:/Users/Hira.Wahid/PycharmProjects/pytestp/downloads')
    return aglog_file

def download_cql():
    t_call_queue_log_file = run("ls -t /data/afiniti/log_tables| grep -i t_call_queue_log  | head -1")
    get('/data/afiniti/log_tables/' + t_call_queue_log_file, 'C:/Users/Hira.Wahid/PycharmProjects/pytestp/downloads')
    return t_call_queue_log_file

def clean_up():
    with settings(
            hide('warnings', 'running', 'stdout', 'stderr'),
            warn_only=True
    ):
        run("rm -f /data/afiniti/log_tables/*")

def start_config_upgrade():
    run("echo y|start-config-upgrade")


def run_itp(script):
    #Place ITP_configuration and scripts in the mentioned paths
    with settings(
            hide('stderr'),
            warn_only=True
    ):
        run("pwd")
        run("docker cp "+config['fabric']['itp_scripts'] + script+" master:/app/afiniti/.")
        #run("docker cp /home/hira.wahid/itp_files/ITP_CONFIGURATION.xml master:/app/afiniti/.")
        run("docker exec -it master ./afiniti_sim -file " + script)

def restart_async():
    run("docker stop async")
    time.sleep(5)
    run("docker start async")

def restart_echi():
    run("docker stop echi_sync")
    time.sleep(5)
    run("docker start echi_sync")




def stop_v6_all():
    with settings(
            hide('warnings', 'running', 'stdout', 'stderr'),
            warn_only=True
    ):
        run("echo y|stop-core-all")
        run("echo y|stop-config")


def start_v6():
    run("echo y|start-v6")

def check_config_upgrade_status():
    return run("dps | grep cf_config")


def check_si_status():
    return run("docker inspect -f '{{.State.Running}}' si").stdout.splitlines()

def stop_config_v():
    with settings(
            hide('warnings', 'stderr'),
            warn_only=True
    ):
        run("echo y|stop-config -v")
