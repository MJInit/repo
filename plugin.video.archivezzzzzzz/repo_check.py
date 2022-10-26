import xbmc
import xbmcgui
import xbmcvfs
import xbmcaddon
import sqlite3
from glob import glob

DB_PATH = xbmcvfs.translatePath('special://home/userdata/Database/')
DB_FILE = glob(DB_PATH + 'Addons*.db')[0]
MY_ADDON = xbmcaddon.Addon().getAddonInfo('id')
SAFE_REPOS = ['repository.mjinit']  # list of allowed repos, keep the empty quotes to allow addon to be installed from zip file
MESSAGE = 'This addon was installed by an unofficial repository.'  # change to whatever you want

def get_origin(addon_id: str):
    response = ''
    try:
        con = sqlite3.connect(DB_FILE)
        cursor = con.cursor()
        cursor.execute('SELECT origin FROM installed WHERE addonID = ?', (addon_id,))
        response = cursor.fetchone()
    except sqlite3.Error as e:
        xbmc.log('%s: There was an error reading the database - %s' % (xbmcaddon.Addon().getAddonInfo('name'), e), xbmc.LOGINFO)
        return ''
    finally:
        try:
            if con:
                con.close()
        except UnboundLocalError as e:
            xbmc.log('%s: There was an error connecting to the database - %s' % (xbmcaddon.Addon().getAddonInfo('name'), e), xbmc.LOGINFO)
    if type(response) == tuple:
        return  response[0]
    return response

def repo_check():
    if not get_origin(MY_ADDON) in SAFE_REPOS:
        xbmcgui.Dialog().ok(xbmcaddon.Addon().getAddonInfo('name'), MESSAGE)
        quit()


"""
###---Usage---###
Quits the addon if the addon was installed by a repo that is not in the safe repos list.
Edit the SAFE_REPOS variable with the addon ids of your repos.
Customize the MESSAGE variable to your liking.
Call the repo_check function at the beginning of your code.
Example using Microjen:
Easiest way is to drop this script into root directory of your addon then import and call it from default.py before the function main() is called.
if __name__ == "__main__":
    from repo_check import repo_check
    repo_check()
    main()
"""