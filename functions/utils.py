"""Collection of utilities used by all cogs."""
import json
import configparser
from discord_slash.utils.manage_commands import create_permission, create_option
from discord_slash.model import SlashCommandPermissionType

config = configparser.ConfigParser()
config.read('cred.ini')

try:
    if config['config']['mode'] == "updates":
        servers = [
            878614900824485900
        ]
    else:
        servers = [
            799253855677579285,
            811552770074738688
        ]
except KeyError:
    print("cred.ini does not exist yet")

privateOption = [
    create_option(
        name="private",
        description="send the message privately?",
        option_type=5,
        required=False
    )
]

def slash_perms(permission):
    """Permission handler used by all commands in the bot; goes through permissions.json to check if the user has permission to use a command."""
    with open("configs/permissions.json", "r") as file:
        data = json.load(file)
    if config['config']['mode'] == "main":
        if permission == "dev":
            permissions = {
                811552770074738688: [
                    create_permission(int(userID), SlashCommandPermissionType.USER, True) for userID in data["developers"]
                ],
                799253855677579285:
                [
                    create_permission(int(userID), SlashCommandPermissionType.USER, True) for userID in data["developers"]
                ]
            }
        elif permission == "banned":
            permissions = {
                811552770074738688:
                [
                    create_permission(int(userID), SlashCommandPermissionType.USER, False) for userID in data["811552770074738688"]["banned"]
                ] +
                [
                    create_permission(int(userID), SlashCommandPermissionType.USER, True) for userID in data["developers"]
                ],
                799253855677579285:
                [
                    create_permission(int(userID), SlashCommandPermissionType.USER, False) for userID in data["799253855677579285"]["banned"]
                ] +
                [
                    create_permission(int(userID), SlashCommandPermissionType.USER, True) for userID in data["developers"]
                ]
            }
        else:
            permissions = {
                811552770074738688:
                [
                    create_permission(int(userID), SlashCommandPermissionType.USER, True) for userID in data["811552770074738688"][permission]
                ] +
                [
                    create_permission(int(userID), SlashCommandPermissionType.USER, True) for userID in data["811552770074738688"]["admin"]
                ] +
                [
                    create_permission(int(userID), SlashCommandPermissionType.USER, False) for userID in data["811552770074738688"]["banned"]
                ] +
                [
                    create_permission(int(userID), SlashCommandPermissionType.USER, True) for userID in data["developers"]
                ],
                799253855677579285:
                [
                    create_permission(int(userID), SlashCommandPermissionType.USER, True) for userID in data["799253855677579285"][permission]
                ] +
                [
                    create_permission(int(userID), SlashCommandPermissionType.USER, True) for userID in data["799253855677579285"]["admin"]
                ] +
                [
                    create_permission(int(userID), SlashCommandPermissionType.USER, False) for userID in data["799253855677579285"]["banned"]
                ] +
                [
                    create_permission(int(userID), SlashCommandPermissionType.USER, True) for userID in data["developers"]
                ]
            }
    elif permission == "dev":
        permissions = {
            878614900824485900: [
                create_permission(int(userID), SlashCommandPermissionType.USER, True) for userID in data["developers"]
            ]
        }
    elif permission == "banned":
        permissions = {
            878614900824485900:
            [
                create_permission(int(userID), SlashCommandPermissionType.USER, False) for userID in data["878614900824485900"]["banned"]
            ] +
            [
                create_permission(int(userID), SlashCommandPermissionType.USER, True) for userID in data["developers"]
            ]
        }
    else:
        permissions = {
            878614900824485900:
            [
                create_permission(int(userID), SlashCommandPermissionType.USER, True) for userID in data["878614900824485900"][permission]
            ] +
            [
                create_permission(int(userID), SlashCommandPermissionType.USER, True) for userID in data["878614900824485900"]["admin"]
            ] +
            [
                create_permission(int(userID), SlashCommandPermissionType.USER, False) for userID in data["878614900824485900"]["banned"]
            ] +
            [
                create_permission(int(userID), SlashCommandPermissionType.USER, True) for userID in data["developers"]
            ]
        }
    return permissions

def ephemeral_check(**kwargs):
    """Checks if the private keyword exists, then checks if it is true."""
    try:
        print(kwargs["private"])
    except KeyError:
        return False
    return kwargs["private"]
