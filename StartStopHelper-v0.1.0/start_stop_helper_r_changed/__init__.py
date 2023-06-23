# -*- coding: utf-8 -*-

import time

from typing import Dict

from mcdreforged.api.types import PluginServerInterface as mcdrserver
from mcdreforged.api.command import *
from mcdreforged.api.utils import Serializable


class Config(Serializable):
    permissions: Dict[str, int] = {
        'help': 3,
        'start': 3,
        'stop': 3,
        'stop_exit': 4,
        'restart': 3,
        'exit': 4,
        'kill': 4,
    }


config: Config

def stop_server():
    mcdrserver.stop()
    time.sleep(10)
    if mcdrserver.is_server_running()==True: 
        time.sleep(60)
        if mcdrserver.is_server_running() == True:
            mcdrserver.logger.warning("服务器似乎并没有关闭...")
            mcdrserver.logger.info("10s后服务端进程将被杀死.")
            time.sleep(10)
            mcdrserver.set_exit_after_stop_flag(False)
            if mcdrserver.is_server_running() == False: 
                mcdrserver.logger.info("服务端已关闭")
            else:
                mcdrserver.set_exit_after_stop_flag(False)
                mcdrserver.kill()
    mcdrserver.logger.info("服务端已关闭.")
    return

def stop_exit_server():
    stop_server()
    mcdrserver.exit()

def restart_server():
    stop_server()
    mcdrserver.start()

def on_load(server: PluginServerInterface, prev_module):
    global config
    config = server.load_config_simple('config.json', target_class=Config)
    permissions = config.permissions
    mcdrserver.logger.info("插件已加载")
    mcdrserver.logger.warning("你使用的并非原版！而是 xieyuen 更改版!")
    mcdrserver.logger.info("若需要原版，请在下面的网址下载（或者用MPM）")
    mcdrserver.logger.info("https://www.mcdreforged.org/plugins/start_stop_helper_r")
    mcdrserver.logger.info("或者用 MPM")
    server.register_help_message(
        '!!server',
        {
            'en_us': 'Start and stop server helper',
            'zh_cn': '开关服助手'
        }
    )
    server.register_command(
        Literal('!!server').
            requires(lambda src: src.has_permission(permissions['help'])).
            runs(
            lambda src: src.reply(server.rtr('start_stop_helper_r.help'))
        ).
            then(
            Literal('start').
                requires(lambda src: src.has_permission(permissions['start'])).
                runs(lambda src: server.start())
        ).
            then(
            Literal('stop').
                requires(lambda src: src.has_permission(permissions['stop'])).
                runs(lambda src: stop_server())
        ).
            then(
            Literal('stop_exit').
                requires(
                lambda src: src.has_permission(permissions['stop_exit'])).
                runs(lambda src: stop_exit_server())
        ).
            then(
            Literal('restart').
                requires(
                lambda src: src.has_permission(permissions['restart'])).
                runs(lambda src: server.restart())
        ).
            then(
            Literal('exit').
                requires(lambda src: src.has_permission(permissions['exit'])).
                runs(lambda src: server.exit())
        ).
            then(
            Literal('kill').
                requires(lambda src: src.has_permission(permissions['kill'])).
                runs(lambda src: server.kill())
        )
    )
