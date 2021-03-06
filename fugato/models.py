# fugato.models
# Models for the fugato app
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Thu Oct 23 14:05:24 2014 -0400
#
# Copyright (C) 2016 District Data Labs
# For license information, see LICENSE.txt
#
# ID: models.py [8eae6c4] benjamin@bengfort.com $

"""
Models for the fugato app.
"""

##########################################################################
## Imports
##########################################################################

import time

from slugify import slugify
from django.db import models
from voting.models import Vote
from operator import itemgetter
from minent.utils import nullable
from autoslug import AutoSlugField
from django.core.urlresolvers import reverse
from model_utils.models import TimeStampedModel
from fugato.managers import QuestionManager, AnswerManager
from django.contrib.contenttypes.fields import GenericRelation


##########################################################################
## Qustion and Answer Models
##########################################################################

class Question(TimeStampedModel):

    text     = models.CharField( max_length=512, null=False )                      # The text of the question
    slug     = AutoSlugField( populate_from='text', slugify=slugify, unique=True ) # The slug of the question
    signature = models.CharField( max_length=28, unique=True, editable=False )     # The normalized signature
    details  = models.TextField( help_text="Edit in Markdown", **nullable )        # Additional details about the question
    details_rendered = models.TextField( editable=False, **nullable )              # HTML rendered details text from MD
    related  = models.ManyToManyField( 'self', editable=True, blank=True )         # Links between related questions
    author   = models.ForeignKey( 'auth.User', related_name='questions' )          # The author of the question
    votes    = GenericRelation( Vote, related_query_name='questions' )             # Vote on whether or not the question is relevant
    tags     = models.ManyToManyField('tagging.Tag', related_name='questions')     # Tag each question with terms for easy lookup

    ## Set custom manager on Question
    objects  = QuestionManager()

    class Meta:
        db_table = "questions"
        get_latest_by = 'created'

    def get_absolute_url(self):
        """
        Return the detail view of the Question object
        """
        return reverse('question', kwargs={'slug': self.slug})

    def get_api_detail_url(self):
        """
        Returns the API detail endpoint for the object
        """
        return reverse('api:question-detail', args=(self.pk,))

    def get_stream_repr(self):
        """
        Returns the object representation for the activity stream.
        """
        return '&ldquo;{}&rdquo;'.format(self)

    def has_tag(self, tag):
        """
        Returns True if the tag (a string) is in the list of tags.
        """
        return tag in [tag.text for tag in self.tags.all()]

    def set_answer_order_by_votes(self):
        """
        A helper function that calls the `set_answer_order` function and
        passes in the order based on the sum of the votes.
        """
        # Construct the aggregation query
        query = self.answers.count_votes().values('id', 'num_votes')

        order = [
            a['id'] for a in sorted(query, key=itemgetter('num_votes'), reverse=True)
        ]

        self.set_answer_order(order)

    def __str__(self):
        return self.text


class Answer(TimeStampedModel):

    text     = models.TextField(                                                 # The text of the answer (markdown)
                null=False, blank=False,
                help_text="Edit in Markdown"
               )
    text_rendered = models.TextField( editable=False, null=False )               # HTML rendered details of the question
    related  = models.ManyToManyField( 'self' )                                  # Links between related responses
    author   = models.ForeignKey( 'auth.User', related_name="answers" )          # The author of the answer
    question = models.ForeignKey( 'fugato.Question', related_name="answers" )    # The question this answer answers
    votes    = GenericRelation( Vote, related_query_name='answers' )             # Votes for the goodness of the answer

    ## Set custom manager on Answer
    objects  = AnswerManager()

    class Meta:
        db_table = "answers"
        order_with_respect_to = 'question'

    def get_absolute_url(self):
        """
        Return the detail view of the Answer object, that is the url of the
        question with the vertical reference to the answer attached.
        """
        url =  self.question.get_absolute_url()
        url += "#answer-{}".format(self.id)
        return url

    def get_api_detail_url(self):
        """
        Returns the API detail endpoint for the object
        """
        return reverse('api:answer-detail', args=(self.pk,))

    def get_stream_repr(self):
        """
        Returns the object representation for the activity stream.
        """
        return self.question.get_stream_repr()

    def __str__(self):
        return self.text
