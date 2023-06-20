# -*- coding: utf-8 -*-

from pytube import YouTube
import os
from bs4 import BeautifulSoup
import requests
from odoo import fields, models, api
from odoo.exceptions import ValidationError


class YoutubeVideo(models.Model):
    _name = "youtube.video"
    _description = "Youtube Video Downloder"
    _rec_name = "video_title"

    video_link = fields.Char(string="Video Link")
    video_title = fields.Char(string="Title", readonly=True)
    state = fields.Selection(
        selection=[
            ("draft", "Draft"),
            ("saved", "Saved"),
            ("downloaded", "Downloaded"),
        ],
        string="Status",
        required=True,
        readonly=True,
        copy=False,
        tracking=True,
        default="draft",
    )
    video_resolution = fields.Selection(
        selection=[
            ("360p", "360p"),
            ("360p", "360p"),
            ("480p", "480p"),
            ("720p", "720p"),
        ],
        string="Resolution",
        default="360p",
        required=True,
    )

    def download_video(self):
        yt = YouTube(self.video_link)
        path = "/home/odoo/Downloads/you_tube"
        streams = (
            yt.streams.filter(progressive=True, file_extension="mp4")
            .order_by("resolution")
            .desc()
        )
        available_resolutions = [stream.resolution for stream in streams]
        if self.video_resolution not in available_resolutions:
            raise ValidationError(
                "Selected resolution is not available to be downloaded. Please select another resolution."
            )

        selected_stream = None
        for stream in streams:
            if stream.resolution == self.video_resolution:
                selected_stream = stream
                break

        if selected_stream is None:
            raise ValidationError(
                "Selected resolution is not available for this video."
            )

        # To check the folder at given path or to create one
        if not os.path.exists(path):
            os.makedirs(path)

        selected_stream.download(output_path=path, filename_prefix="youtube_video")
        self.write({"state": "downloaded"})

    # To get the title of the video
    @api.model
    def create(self, vals):
        res = super(YoutubeVideo, self).create(vals)
        response = requests.get(res.video_link)
        soup = BeautifulSoup(response.content, "html.parser")
        res.video_title = soup.find("title").text
        res.write({"state": "saved"})
        return res
