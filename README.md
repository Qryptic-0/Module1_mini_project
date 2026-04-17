# Module1_mini_project
HOW TO USE


As this is a command line interface, it is run by calling the script followed by its command and arguments.
For instance, to 'List everything', this command is used: python http_explorer.py list posts
to 'Get one item', this command is used:  python http_explorer.py get posts 1
to 'Create a post', this command is used: python http_explorer.py create --title "My Title" --body "My Content" --user-id 1
for a Partial Update, this command line can be used:  python http_explorer.py update 1 --title "New Title"
to perform a Full Update, this command is used: python http_explorer.py update 1 --title "New" --body "New" --full
to 'Delete', use: python http_explorer.py delete 1
and to, 'Check Stats', usee the following: python http_explorer.py stats
