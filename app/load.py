from typing import Dict, Union

from yaml import load

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper
from app.helpers import set_gravatar, load_pages, load_roles

ICON_CLASS = '<i class="fas fa-globe"></i>'


def get_settings(
    compile_site: bool, local: bool, settings_file: str
) -> Dict[str, Union[str, bool, int]]:
    """
    Gets the site setting from config.yaml

    :return: Dictionary containing information to drive the creation of the static type
    """
    settings = load(open(settings_file), Loader=Loader)
    settings["cname"] = settings["url"]
    settings["local"] = local
    settings["avatar_default"] = settings.get(
        "avatar_default", "assets/media/avatar.jpg"
    )
    settings["avatar_size"] = 250
    if not compile_site:
        settings["url"] = "http://localhost:4242"
    return settings


def get_global(
    compile_site=False,
    local=False,
    settings_file="config.yaml",
    about_file="resume/about.yaml",
):
    settings = get_settings(compile_site, local, settings_file)

    # Load can take the open file handle, read is default mode
    about = load(open(about_file), Loader=Loader)

    about["gravatar"] = set_gravatar(
        about["contact"]["email"],
        settings["avatar_default"],
        settings["avatar_size"],
    )

    links = {}

    # Use get to provide a default if not present, empty list in this case
    all_links = about.get("links", [])
    for link in all_links:
        if isinstance(all_links[link], dict):
            fresh_link = all_links[link]

            # If it doesn't exists, returns false and set default
            if not fresh_link.get("text", False):
                fresh_link["text"] = fresh_link["url"]

            if not fresh_link.get("icon", False):
                fresh_link["icon"] = ICON_CLASS
        else:
            fresh_link = {
                "url": all_links[link],
                "text": all_links[link],
                "icon": ICON_CLASS,
            }

        links[fresh_link["url"]] = fresh_link

    about["links"] = links

    # Get pages for navigation
    nav = {}
    pages = load_pages()
    set_pages = {}
    for page in pages:
        p = pages[page]
        # TODO: Optional page exclusion
        title = p["meta"].get("title")
        if "anchor" in p["meta"]:
            title = p["meta"].get("anchor")
        set_pages[p["filename"]] = {
            "href": settings["url"] + "/" + p["filename"],
            "anchor": title,
            "order": p["meta"].get("order") if "order" in p["meta"] else 2,
        }
    sort_pages = sorted(set_pages.items(), key=lambda x: x[1]["order"])
    for i, p in sort_pages:
        nav[i] = p
    settings["nav"] = nav
    # Get roles
    settings["roles"] = load_roles()
    site = {
        "site": settings,
        "person": about,
    }
    return site
