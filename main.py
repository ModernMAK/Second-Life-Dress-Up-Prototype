# Blocking out the website, setting up the environment (endpoints, directories
# 2:33 => 2:57 ~ 24
# 3:14 => 3:44 ~ 30
# 4:05 => 4:23 ~ 18

# Moved to sticky instead of position fixed
# Setup handlebars, jquery, first script working as intended
# Jscript to load images
# 12:06 => 1:12 ~ 66
# 1:30 => 1:45 ~ 15

# 3:16 => 3:56 ~ 40 ~ (JS to select update previews)
# 6:01 => 6:13 ~ 12 ~ (Cookies)
# 6:13 => 6:22 ~ 11 ~ Layout
# 6:28 => 7:02 ~ 34 ~ Borders + Scrolling
# 7:09 => 8:12 ~ 63 ~ Code Review
# 313 / 60 ~ $200
from http import HTTPStatus
from typing import Tuple, Any, Dict

import uvicorn
from fastapi import FastAPI

# this could be replicated by serving from www (or public html root) and using jscript
#   Cookies or get args could be used to cache state
from starlette.responses import Response, JSONResponse, RedirectResponse, HTMLResponse
from starlette.staticfiles import StaticFiles


def dupe(d: Dict[int, str], dupes: int = 2) -> Dict[int, str]:
    temp = {}
    for key in d:
        for i in range(dupes):
            temp[key + i * len(d)] = d[key]
    return temp


def dual_dupe(d: Dict[Tuple[int, int], str], dupe_top: int = 2, dupe_bot: int = 2, top_count: int = 2, bot_count: int = 2):
    temp = {}
    for (tkey, bkey) in d:
        for i in range(dupe_top):
            for j in range(dupe_bot):
                temp[(tkey + i * top_count, bkey + j * bot_count)] = d[(tkey, bkey)]
    return temp


def add_routes(application: FastAPI):
    @application.get("/")
    def index():
        f_path = "static/html/index.html"
        with open(f_path) as handle:
            return HTMLResponse(handle.read())

    # Somehow the server needs to tell me all bottoms right?
    # I assume theres an endpoint somewhere for this
    #   Preferably a microservice with a CDN
    #       I'd use CORS to restrict access (if you want to restrict access to the images)
    #           This avoids the need of the webpage having some kind of auth
    _bottoms: Dict[int, str] = {
        0: r"/img/bottoms/bot_pants_jeans.jpg",
        1: r"/img/bottoms/bot_shorts_idk.jpg",
    }

    _bottoms = dupe(_bottoms, 12)
    # temp = {}
    # for key in _bottoms:
    #     for i in range(4):
    #         temp[key+i*2] = _bottoms[key]
    # _bottoms = temp

    _tops: Dict[int, str] = {
        0: r"/img/tops/top_jacket_winterized.jpg",
        1: r"/img/tops/top_shirt_adidas.jpg"
    }
    _tops = dupe(_tops, 12)

    # TOP, BOT
    _displays: Dict[Tuple[int, int], str] = {
        (0, 0): r"/img/previews/display_jwinter_jeans.jpg",
        (0, 1): r"/img/previews/display_jwinter_shorts.jpg",
        (1, 0): r"/img/previews/display_adidas_jeans.jpg",
        (1, 1): r"/img/previews/display_adidas_shorts.jpg",
    }

    _displays = dual_dupe(_displays, 12, 12, 2, 2)

    def add_group(path: str, items: Dict[int, Any]):
        @application.get(path)
        def group(id: int = None, img: bool = False):
            try:
                if id:
                    path = items[id]
                    if img:
                        return RedirectResponse(path, HTTPStatus.SEE_OTHER)
                    else:
                        return JSONResponse(path)
                else:
                    return JSONResponse(items)
            except KeyError:
                return Response(status_code=404)

    add_group("/bottoms", _bottoms)
    add_group("/tops", _tops)

    @application.get("/preview")
    def preview(top: int, bot: int, img: bool = True):
        try:
            path = _displays[(top, bot)]
            if img:
                # I use a redirect so that images can be cached (since images are served from static
                return RedirectResponse(path, HTTPStatus.SEE_OTHER)
            else:
                return JSONResponse(path)
        except KeyError:
            return Response(status_code=404)

    application.mount("/img", StaticFiles(directory="static/img"))
    application.mount("/js", StaticFiles(directory="static/js"))


def run():
    app = FastAPI()
    add_routes(app)
    uvicorn.run(app, port=80)


if __name__ == "__main__":
    run()
