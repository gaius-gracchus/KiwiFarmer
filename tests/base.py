# -*- coding: UTF-8 -*-

"""Tests for to kiwifarms.functions module
"""

###############################################################################

import os

import pytest

from kiwifarmer import (
  base,
  functions, )

###############################################################################

def test_Thread( resources ):

  thread = base.Thread( input = resources[ 'soup' ] )

  thread_insertion = thread.thread_insertion

###############################################################################

def test_Page( resources ):

  page = base.Page( input = resources[ 'soup' ] )

  post_soups = page.get_post_soups( )

###############################################################################

def test_Post( resources ):

  post = base.Post( post_soup = resources[ 'post' ] )

  post_insertion = post.post_insertion
  blockquote_insertions = post.blockquote_insertions
  link_insertions = post.link_insertions
  image_insertions = post.image_insertions

###############################################################################