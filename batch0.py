#!/usr/bin/env python3

import iterm2
import AppKit

# Launch the app
AppKit.NSWorkspace.sharedWorkspace().launchApplication_("iTerm2")

async def main(connection):
    app = await iterm2.async_get_app(connection)

    # Foreground the app
    await app.async_activate()

    # Create a new window
    myterm = await iterm2.Window.async_create(connection)
    await myterm.async_activate()

    # Create Panes
    pane1 = myterm.current_tab.current_session
    pane2 = await pane1.async_split_pane(vertical=False)
    pane3 = await pane1.async_split_pane(vertical=True)
    pane4 = await pane2.async_split_pane(vertical=True)

    # Server List
    server_list = [
        {
            'addr': '<server1>',
            'session': pane1
        },
        {
            'addr': '<server2>',
            'session': pane2
        },
        {
            'addr': '<server3>',
            'session': pane3
        },
        {
            'addr': '<server4>',
            'session': pane4
        }
    ]

    
    for server in server_list:
        await server['session'].async_send_text("ssh '{}' \n".format(server['addr']))
        await server['session'].async_send_text('cd /var/puppet_manifests \n')
        await server['session'].async_send_text('tmux \n')

# Passing True for the second parameter means keep trying to
# connect until the app launches.
iterm2.run_until_complete(main, True)
