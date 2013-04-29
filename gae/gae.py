"""
This code was started from the examples at: 

https://github.com/GoogleCloudPlatform/appengine-crowdguru-python/blob/master/guru.py
"""
import datetime

from google.appengine.api import datastore_types
from google.appengine.api import xmpp
from google.appengine.ext import ndb
from google.appengine.ext.webapp import xmpp_handlers
import webapp2
from webapp2_extras import jinja2

PONDER_MSG = 'Hmm. Let me think on that a bit.'
TELLME_MSG = 'While I\'m thinking, perhaps you can answer me this: {}'
SOMEONE_ANSWERED_MSG = ('We seek those who are wise and fast. One out of two '
                        'is not enough. Another has answered my question.')
ANSWER_INTRO_MSG = 'You asked me: {}'
ANSWER_MSG = 'I have thought long and hard, and concluded: {}'
WAIT_MSG = ('Please! One question at a time! You can ask me another once you '
            'have an answer to your current question.')
THANKS_MSG = 'Thank you for your wisdom.'
TELLME_THANKS_MSG = THANKS_MSG + ' I\'m still thinking about your question.'
EMPTYQ_MSG = 'Sorry, I don\'t have anything to ask you at the moment.'
HELP_MSG = ('I am the amazing Crowd Guru. Ask me a question by typing '
            '\'/tellme the meaning of life\', and I will answer you forthwith! '
            'To learn more, go to {}/')
MAX_ANSWER_TIME = 120


class IMProperty(ndb.StringProperty):
    """A custom property for handling IM objects.

    IM or Instant Message objects include both an address and its protocol. The
    constructor and __str__ method on these objects allow easy translation from
    type string to type datastore_types.IM.
    """

    def _validate(self, value):
        """Validator to make sure value is an instance of datastore_types.IM.

        Args:
            value: The value to be validated. Should be an instance of
                datastore_types.IM.

        Raises:
            TypeError: If value is not an instance of datastore_types.IM.
        """
        if not isinstance(value, datastore_types.IM):
            raise TypeError('expected an IM, got {!r}'.format(value))

    def _to_base_type(self, value):
        """Converts native type (datastore_types.IM) to datastore type (string).

        Args:
            value: The value to be converted. Should be an instance of
                datastore_types.IM.

        Returns:
            String corresponding to the IM value.
        """
        return str(value)

    def _from_base_type(self, value):
        """Converts datastore type (string) to native type (datastore_types.IM)
        Args:
            value: The value to be converted. Should be a string.
        Returns:
            String corresponding to the IM value.
        """
        return datastore_types.IM(value)


def bare_jid(sender):
    """Identify the user by bare jid.
    See http://wiki.xmpp.org/web/Jabber_Resources for more details.
    Args:
        sender: String; A jabber or XMPP sender.
    Returns:
        The bare Jabber ID of the sender.
    """
    return sender.split('/')[0]


class XmppHandler(xmpp_handlers.CommandHandler):
    """Handler class for all XMPP activity."""

    def unhandled_command(self, message=None):
        """Shows help text for commands which have no handler.
        Args:
            message: xmpp.Message: The message that was sent by the user.
        """
        message.reply(HELP_MSG.format(self.request.host_url))

    def askme_command(self, message=None):
        """Responds to the /askme command.
        Args:
            message: xmpp.Message: The message that was sent by the user.
        """
        im_from = datastore_types.IM('xmpp', bare_jid(message.sender))
        currently_answering = Question.get_answering(im_from)
        question = Question.assign_question(im_from)
        if question:
            message.reply(TELLME_MSG.format(question.question))
        else:
            message.reply(EMPTYQ_MSG)
        # Don't unassign their current question until we've picked a new one.
        if currently_answering:
            currently_answering.unassign(im_from)

    def text_message(self, message=None):
        """Called when a message not prefixed by a /cmd is sent to the XMPP bot
        Args:
            message: xmpp.Message: The message that was sent by the user.
        """
        im_from = datastore_types.IM('xmpp', bare_jid(message.sender))
        question = None #Question.get_answering(im_from)
        if question:
            pass
            # other_assignees = question.assignees
            # other_assignees.remove(im_from)

            # # Answering a question
            # question.answer = message.arg
            # question.answerer = im_from
            # question.assignees = []
            # question.answered = datetime.datetime.now()
            # question.put()

            # # Send the answer to the asker
            # xmpp.send_message([question.asker.address],
            #                   ANSWER_INTRO_MSG.format(question.question))
            # xmpp.send_message([question.asker.address],
            #                   ANSWER_MSG.format(message.arg))

            # # Send acknowledgement to the answerer
            # asked_question = Question.get_asked(im_from)
            # if asked_question:
            #     message.reply(TELLME_THANKS_MSG)
            # else:
            #     message.reply(THANKS_MSG)

            # # Tell any other assignees their help is no longer required
            # if other_assignees:
            #     xmpp.send_message([user.address for user in other_assignees],
            #                       SOMEONE_ANSWERED_MSG)
        else:
            self.unhandled_command(message)

    def tellme_command(self, message=None):
        """Handles /tellme requests, asking the Guru a question.

        Args:
            message: xmpp.Message: The message that was sent by the user.
        """
        im_from = datastore_types.IM('xmpp', bare_jid(message.sender))
        # asked_question = Question.get_asked(im_from)

        # if asked_question:
        #     # Already have a question
        #     message.reply(WAIT_MSG)
        # else:
        #     # Asking a question
        #     asked_question = Question(question=message.arg, asker=im_from)
        #     asked_question.put()

        #     currently_answering = Question.get_answering(im_from)
        #     if not currently_answering:
        #         # Try and find one for them to answer
        #         question = Question.assign_question(im_from)
        #         if question:
        #             message.reply(TELLME_MSG.format(question.question))
        #             return
        message.reply(PONDER_MSG)


class XmppPresenceHandler(webapp2.RequestHandler):
    """Handler class for XMPP status updates."""

    def post(self, status):
        """POST handler for XMPP presence.

        Args:
            status: A string which will be either available or unavailable
               and will indicate the status of the user.
        """
        sender = self.request.get('from')
        im_from = datastore_types.IM('xmpp', bare_jid(sender))
        suspend = (status == 'unavailable')
        query = Question.filter(Question.asker == im_from,
                                Question.answer == None,
                                Question.suspended == (not suspend))
        question = query.get()
        if question:
            question.suspended = suspend
            question.put()


class LatestHandler(webapp2.RequestHandler):
    """Displays the most recently answered questions."""

    @webapp2.cached_property
    def jinja2(self):
        """Cached property holding a Jinja2 instance.

        Returns:
            A Jinja2 object for the current app.
        """
        return jinja2.get_jinja2(app=self.app)

    def render_response(self, template, **context):
        """Use Jinja2 instance to render template and write to output.

        Args:
            template: filename (relative to $PROJECT/templates) that we are
                rendering.
            context: keyword arguments corresponding to variables in template.
        """
        rendered_value = self.jinja2.render_template(template, **context)
        self.response.write(rendered_value)

    def get(self):
        """Handler for latest questions page."""
        query = Question.query(Question.answered > None).order(
                -Question.answered)
        self.render_response('latest.html', questions=query.fetch(20))

APPLICATION = webapp2.WSGIApplication([
        ('/', LatestHandler),
        ('/_ah/xmpp/message/chat/', XmppHandler),
        ('/_ah/xmpp/presence/(available|unavailable)/', XmppPresenceHandler),
        ], debug=True)
