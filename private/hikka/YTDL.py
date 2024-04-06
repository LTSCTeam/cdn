#  Copyright (c) 2023 Dmertixddd aka Tokyani
#  All rights reserved.
#  This code, including all of its parts, is the property of Dmertixddd aka Tokyani and is protected by copyright law.
#  Owner: Dmertixddd aka Tokyani
#  Contact: dmertixddd.t.me
#
#  Permission is granted to use, modify, and distribute this code only with explicit written permission from the owner.
#  Violation of copyright may result in legal consequences.

# meta developer: @dmertixddd

# requires: yt-dlp, ffmpeg

import os

from telethon.tl.types import DocumentAttributeAudio
from yt_dlp import YoutubeDL
from yt_dlp.utils import (
    ContentTooShortError,
    DownloadError,
    ExtractorError,
    GeoRestrictedError,
    MaxDownloadsReached,
    PostProcessingError,
    UnavailableVideoError,
    XAttrMetadataError,
)

from .. import loader, utils


@loader.tds
class YtDlMod(loader.Module):
    """YouTube Downloader Module"""

    strings = {
        "name": "YTDL",
        "preparing": "<b>[YT-Dl]</b> Preparing...",
        "downloading": "<b>[YT-Dl]</b> Downloading...",
        "working": "<b>[YT-Dl]</b> Working...",
        "exporting": "<b>[YT-Dl]</b> Exporting...",
        "reply": "<b>[YT-Dl]</b> No link!",
        "noargs": "<b>[YT-Dl]</b> No args!",
        "content_too_short": "<b>[YT-Dl]</b> Downloading content too short!",
        "geoban": "<b>[YT-Dl]</b> The video is not available "
        "for your geographical location due to geographical "
        "restrictions set by the website!",
        "maxdlserr": '<b>[YT-Dl]</b> The download limit is as follows: " oh ahah"',
        "pperr": "<b>[YT-Dl]</b> Error in post-processing!",
        "noformat": "<b>[YT-Dl]</b> Media is not available in "
        "the requested format",
        "xameerr": "<b>[YT-Dl]</b> {0.code}: {0.msg}\n{0.reason}",
        "exporterr": "<b>[YT-Dl]</b> Error when exporting video",
        "err": "<b>[YT-Dl]</b> {}",
        "err2": "<b>[YT-Dl]</b> {}: {}",
    }

    async def ytvidcmd(self, m):
        """ <link / reply_to_link> - download video"""
        await self.riper(m, "video")

    async def ytaudcmd(self, m):
        """ <link / reply_to_link> - download audio"""
        await self.riper(m, "audio")

    async def riper(self, m, type):
        reply = await m.get_reply_message()
        args = utils.get_args_raw(m)
        url = args or reply.raw_text
        if not url:
            return await utils.answer(m, self.strings("noargs", m))
        m = await utils.answer(m, self.strings("preparing", m))
        if type == "audio":
            opts = {
                "format": "bestaudio",
                "addmetadata": True,
                "key": "FFmpegMetadata",
                "writethumbnail": True,
                "prefer_ffmpeg": True,
                "geo_bypass": True,
                "nocheckcertificate": True,
                "postprocessors": [
                    {
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "mp3",
                        "preferredquality": "320",
                    }
                ],
                "outtmpl": "%(id)s.mp3",
                "quiet": True,
                "logtostderr": False,
            }
            video = False
            song = True
        elif type == "video":
            opts = {
                "format": "best",
                "addmetadata": True,
                "key": "FFmpegMetadata",
                "prefer_ffmpeg": True,
                "geo_bypass": True,
                "nocheckcertificate": True,
                "postprocessors": [
                    {"key": "FFmpegVideoConvertor", "preferedformat": "mp4"}
                ],
                "outtmpl": "%(id)s.mp4",
                "logtostderr": False,
                "quiet": True,
            }
            song = False
            video = True
        try:
            await utils.answer(m, self.strings("downloading", m))
            with YoutubeDL(opts) as rip:
                rip_data = rip.extract_info(url)
        except DownloadError as DE:
            return await utils.answer(m, self.strings("err", m).format(str(DE)))
        except ContentTooShortError:
            return await utils.answer(m, self.strings("content_too_short", m))
        except GeoRestrictedError:
            return await utils.answer(m, self.strings("geoban", m))
        except MaxDownloadsReached:
            return await utils.answer(m, self.strings("maxdlserr", m))
        except PostProcessingError:
            return await utils.answer(m, self.strings("pperr", m))
        except UnavailableVideoError:
            return await utils.answer(m, self.strings("noformat", m))
        except XAttrMetadataError as XAME:
            return await utils.answer(m, self.strings("xameerr", m).format(XAME))
        except ExtractorError:
            return await utils.answer(m, self.strings("exporterr", m))
        except Exception as e:
            return await utils.answer(
                m, self.strings("err2", m).format(str(type(e)), str(e))
            )
        if song:
            u = rip_data["uploader"] if "uploader" in rip_data else "Northing"
            await utils.answer(
                m,
                open(f"{rip_data['id']}.mp3.mp3", "rb"),
                supports_streaming=True,
                reply_to=reply.id if reply else None,
                attributes=[
                    DocumentAttributeAudio(
                        duration=int(rip_data["duration"]),
                        title=str(rip_data["title"]),
                        performer=u,
                    )
                ],
            )
            os.remove(f"{rip_data['id']}.mp3.mp3")
        elif video:
            await utils.answer(
                m,
                open(f"{rip_data['id']}.mp4", "rb"),
                reply_to=reply.id if reply else None,
                supports_streaming=True,
                caption=rip_data["title"],
            )
            os.remove(f"{rip_data['id']}.mp4.mp4")
            os.remove(f"{rip_data['id']}.webp")