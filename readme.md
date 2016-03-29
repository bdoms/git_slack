Copyright &copy; 2016, [Brendan Doms](http://www.bdoms.com/)  
Licensed under the [MIT license](http://www.opensource.org/licenses/MIT)  


# Git Slack

A hook to automatically notify Slack when a git push happens.


## A Simple Use Case

You are creating a new release of your product.
This *usually* happens simultaneously with pushing to a branch.
Developers and others who get notified of pushes might know about this,
but non-technical people probably don't.
And there might not be a good list of what's changed.

Time to increase visibility.

This pre-push hook notifies Slack that a new release is going out,
and it optionally provides a list of included changes in the form of Trello cards.


## Setup

Copy the `pre-push` file to your repo's `.git/hooks/pre-push`
or integrate it with an existing file if you already have one.
Make sure that the import line will work correctly for where you put this project.
Then replace all of the arguments in the hook with your own values.
See the [Slack submodule](https://github.com/bdoms/slack)
for instructions on creating the webhook for the `url` parameter.


### Optional Arguments

#### `branch`

By default all branches are considered valid,
but if you specify one then only pushes for that branch send notifications.
Typically you would set this to `master` to only notify when that branch is pushed.

#### `remote`

By default all remotes are considered valid,
but if you specify one then only pushes to that remote send notifications.
For example, you might set this to `heroku` to only notify when pushing to that remote.

#### `message`

Defaults to `New release deployed by %s` where the current git username is interpolated.

#### `verbose`

By default printing is suppressed.
Set `verbose` to `True` to get more information about all the actions being taken.


### Runtime Options

#### `trello_cards`

If included, this should be a list of JSON-style dictionaries representing Trello cards.
They will be attached to the Slack message as a list of short names, each linking to the relevant card.
They will be styled as an unordered list, but they will still preserve their order when displayed.

#### `trello_colors`

If the provided cards have labels then the colors can be included as part of the Slack message.
As these colors can be changed by the user, you must provide them for this feature to work.
They should be formatted as a dictionary of color names to hex color values.
To see an example, my [Trello project](https://github.com/bdoms/trello)
includes [the default set](https://github.com/bdoms/trello/blob/master/__init__.py#L6-L9).
