import sys

from .lib.slack import Slack
from .lib import git


class GitSlackHook(object):

    def __init__(self, url='', branch='', remote='',
        message='New release deployed by %s', verbose=False):

        if not url: sys.exit('Slack: url is required - aborting.')

        self.client = Slack(url)
        self.branch = branch
        self.remote = remote
        self.message = message
        self.verbose = verbose

    def pre_push(self, trello_cards=None, trello_colors=None):
        # only talk to Slack if one of the specified branches is being pushed
        # e.g. take action on master but not on a feature branch
        current_branch = git.currentBranch()
        if self.branch and current_branch != self.branch:
            if self.verbose:
                print('Slack: pushing unspecified branch skips notification')
            return

        # also skip if a remote is specified but we're not pushing to it
        # e.g. pushing to github but release is to heroku
        push_remote = git.pushRemote()
        if self.remote and push_remote != self.remote:
            if self.verbose:
                print('Slack: pushing to unspecified remote skips notification')
            return

        username = git.currentUser()
        text = self.message % username
        attachments = []

        if trello_cards:
            text += ':'

            for card in trello_cards:
                fallback = '#' + str(card['idShort']) + ' - ' + card['name']
                card_text = '<' + card['url'] + '|#' + str(card['idShort']) + '> ' + card['name']
                attachment = {'fallback': fallback, 'text': card_text}

                if trello_colors and 'labels' in card:
                    # just pick the first label we can find to color since Slack only supports one
                    for label in card['labels']:
                        color_name = label['color']
                        if color_name in trello_colors:
                            attachment['color'] = trello_colors[color_name]
                            break
                        elif self.verbose:
                            print('Slack: no value found for color named "%s"' % color_name)

                attachments.append(attachment)

        if self.verbose:
            print('Slack: ' + text + ' ' + str(len(attachments)) + ' card(s)')

        self.client.postMessage(text, attachments=attachments)
