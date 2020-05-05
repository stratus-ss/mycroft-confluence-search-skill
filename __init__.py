from telegram.ext import Updater
from atlassian import Confluence
from mycroft.skills.core import MycroftSkill, intent_file_handler
from mycroft.util.log import getLogger
import time

class MycroftConfluenceSearch(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        self.all_confluence_search_results = ''
        self.delete_these_results = []
        self.parse_these_results = {}

    def _establish_confluence_connection(self):
        """
        Setup the confluence object to be interacted with later
        :return:
        """
        # URL needs to be in the settingsmeta.yaml
        # confluence username needs to be in the settingsmeta.yaml
        # confluence password needs to be in the settingsmeta.yaml
        self.username = self.settings.get('user_name')
        self.password = self.settings.get('password')
        self.confluence_url = self.settings.get('confluence_url')
        self.confluence = Confluence(
            url=self.confluence_url,
            username=self.username,
            password=self.password)

    def _setup_telegram_bot(self):
        """
        Sets up the telegram bot key and the channel id to post to
        :return: Nothing
        """
        # Setup the telegram bot
        # botkey needs to be in the settingsmeta.yaml
        self.botkey = self.settings.get('telegram_bot_key')
        self.updater = Updater(token=self.botkey, use_context=True)
        # chat_id needs to be in the settingsmeta.yaml
        self.chat_id = self.settings.get('telegram_chat_id')

    def create_url_dict(self, confluence_search_results):
        """
        This is used to create a dictionary of results so that we can parse it later
        :param confluence_search_results: This is a json dict that is obtained from confluence
        :return: A simplified dictionary with the key equal to the Page Title and the URL for the user to click on
        """

        results_dict = {}
        for individual_result in confluence_search_results['results']:
            results_dict[individual_result['title']] = self.confluence.url + individual_result['_links']['webui']
        return results_dict

    def handle_display_more_context(self):
        """
        This function deletes already processed items from the all_confluence_search_results object
        Then if there are items left in the list, it calls the process_url_list() to create a loop
        :return:
        """
        for entry in self.delete_these_results:
            del self.all_confluence_search_results[entry]
        if len(self.all_confluence_search_results) > 0:
            self.process_url_list()

    def process_url_list(self):
        """
        This function loops over the confluence list in order to send them to Telegram
        It also tracks the items that have sent to Telegram.
        Finally, it asks the user whether they want more urls to be displayed
        :return: Nothing
        """
        self.delete_these_results = []
        for index, title in enumerate(self.all_confluence_search_results):
            text = "%s \n%s" % (title, self.all_confluence_search_results[title])
            self.send_message_to_chat(text)
            self.delete_these_results.append(title)
            # Only send 2 entries at a time. Once we get to the second index, break the loop
            if (index + 1) % 2 == 0:
                break
        # wait for a few seconds to let the user review the results so they know
        # whether they got the page they wanted
        time.sleep(5)
        if len(self.all_confluence_search_results) > 2:
            response = self.get_response("Would you like to display more results?")
            if response == "no" or response == "nope" or response is None:
                exit()
            self.handle_display_more_context()

    def send_message_to_chat(self, text):
        self.updater.bot.send_message(chat_id=self.chat_id, text=text)

<<<<<<< HEAD
    def setup_telegram_bot(self):
        # Setup the telegram bot
        # botkey needs to be in the settingsmeta.yaml
        self.botkey = ''
        self.updater = Updater(token=self.botkey, use_context=True)
        # chat_id needs to be in the settingsmeta.yaml
        self.chat_id = ""

    def search_confluence(self):
        # URL needs to be in the settingsmeta.yaml
        # confluence username needs to be in the settingsmeta.yaml
        # confluence password needs to be in the settingsmeta.yaml
        self.confluence = Confluence(
            url="",
            username="",
            password="")

    @intent_handler(IntentBuilder('SearchTitle').require('SearchKeyword').require("Title").optionally("Parent"))
    @adds_context("DisplayMoreResults")
    def handle_search_confluence_title(self, message):
        print(message.data)
        self.setup_telegram_bot()
        self.search_confluence()
        user_specified_title = message.data.get('Title')
=======
    @intent_file_handler("search.confluence.intent")
    def handle_search_confluence_title(self, message):
        """
        This is the main function. It searches confluence for a title containing the user-provided search terms
        It optionally filters the results based on the parent page specified by the user
        :param message: Mycroft data
        :return: Nothing
        """
        self._setup_telegram_bot()
        self._establish_confluence_connection()
        user_specified_title = message.data.get('page')
        # The parent page is optional, it will be None if not determined by the intent
        parent_page = message.data.get('parentpage')
>>>>>>> updated __init__.py to remove the adapt intent and regex

        url = 'rest/api/content/search'
        params = {}
        params['cql'] = 'type={type} AND title~"{title}"'.format(type='page', title=user_specified_title)
        params['start'] = 0
        params['limit'] = 10
<<<<<<< HEAD

        print(">>>>>>>>>>>>> %s" % user_specified_title)

=======
        # call the atlassian library to get a list of all the possible title matches
>>>>>>> updated __init__.py to remove the adapt intent and regex
        response = self.confluence.get(url, params=params)
        # Do some extra work if we need to narrow the results by the parent page
        if parent_page is not None:
            self.parse_these_results['results'] = []
            for individual_page_results in response['results']:
                page_id = individual_page_results['id']
                # get the parent page information
                parent_content = (
                            (self.confluence.get_page_by_id(page_id=page_id, expand='ancestors').get('ancestors')))
                # loop over the parent page titles and see if they match the user's utterance
                for parent_page_results in parent_content:
                    if parent_page.lower() == parent_page_results['title'].lower():
                        self.parse_these_results['results'].append(individual_page_results)
            text = "Under the heading: %s \nI found the following results for the search containing: %s " \
                   % (parent_page.upper(), user_specified_title.upper())
        else:
            self.parse_these_results = response
            text = "I found the following results for the search containing: %s" % user_specified_title.upper()

        self.all_confluence_search_results = self.create_url_dict(self.parse_these_results)
        print(self.all_confluence_search_results)
        self.send_message_to_chat(text)
        self.process_url_list()


def create_skill():
    return MycroftConfluenceSearch()

