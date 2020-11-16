# -*- coding: UTF-8 -*-

"""Tests for to kiwifarms.base module.

The full set of tests for this module can be evaluated by executing the
command::

  $ python -m pytest tests/base.py

from the project root directory.

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

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

def test_Page( resources ):

  page = base.Page( input = resources[ 'soup' ] )

  post_soups = page.get_post_soups( )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

def test_Post( resources ):

  post = base.Post( post_soup = resources[ 'post' ] )

  post_insertion = post.post_insertion
  blockquote_insertions = post.blockquote_insertions
  link_insertions = post.link_insertions
  image_insertions = post.image_insertions

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

def test_ReactionPage( resources ):

  reaction_page = base.ReactionPage( soup = resources[ 'reaction_page' ] )

  reaction_list = reaction_page.get_reaction_soups( )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

def test_Reaction( resources ):

  reaction = base.Reaction(
    reaction_soup = resources[ 'reaction' ], post_id = 12 )

  reaction_insertion = reaction.reaction_insertion

###############################################################################