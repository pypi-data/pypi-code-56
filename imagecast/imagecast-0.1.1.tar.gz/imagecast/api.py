# -*- coding: utf-8 -*-
# (c) 2020 Andreas Motl <andreas@hiveeyes.org>
# License: GNU Affero General Public License, Version 3


def start_service(listen_address):
    host, port = listen_address.split(':')
    port = int(port)
    from uvicorn.main import run
    run(app='imagecast.api:app', host=host, port=port, reload=True)
