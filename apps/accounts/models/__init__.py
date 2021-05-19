# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# to custom the Auth User Model
# you need to import that model into this __init__.py file
# because we use the folder to manage it models.py
from .user import User, Profile

__all__ = (
    'User',
    'Profile',
)
