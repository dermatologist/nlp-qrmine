# -*- coding: utf-8 -*-
from pkg_resources import get_distribution, DistributionNotFound

from .content import Content
from .nlp_qrmine import Qrmine
from .network import Network
from .readfiles import ReadData
from .sentiment import Sentiment
from .mlqrmine import MLQRMine

try:
    # Change here if project is renamed and does not equal the package name
    dist_name = 'qrmine'
    __version__ = get_distribution(dist_name).version
except DistributionNotFound:
    __version__ = 'unknown'
