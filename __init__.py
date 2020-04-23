from telegram.ext import Updater
from atlassian import Confluence
from mycroft.skills.core import MycroftSkill, intent_handler
from mycroft.skills.context import adds_context, removes_context
from mycroft.util.log import getLogger
from adapt.intent import IntentBuilder


class MycroftConfluenceSearch(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        self.all_confluence_search_results = ''
        self.delete_these_results = []

    def create_url_dict(self, confluence_search_results):

        results_dict = {}
        for individual_result in confluence_search_results['results']:
            results_dict[individual_result['title']] = self.confluence.url + individual_result['_links']['webui']
        return results_dict

    def process_url_list(self):
        self.delete_these_results = []
        for index, title in enumerate(self.all_confluence_search_results):
            text="%s \n%s" % (title, self.all_confluence_search_results[title])
            self.send_message_to_chat(text)
            self.delete_these_results.append(title)
            if (index + 1) % 2 == 0:
                if len(self.all_confluence_search_results) <=2:
                    break
                else:
                    self.speak("Would you like to see additional pages?", expect_response=True)
                break

    def send_message_to_chat(self, text):
        self.updater.bot.send_message(chat_id=self.chat_id, text=text)

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

        url = 'rest/api/content/search'
        params = {}
        params['cql'] = 'type={type} AND title~"{title}"'.format(type='page',title=user_specified_title)
        params['start'] = 0
        params['limit'] = 10

        print(">>>>>>>>>>>>> %s" % user_specified_title)

        response = self.confluence.get(url, params=params)
        self.all_confluence_search_results = self.create_url_dict(response)
        text = "I found the following results for the search containing: %s" % user_specified_title
        self.send_message_to_chat(text)
        self.process_url_list()

    @intent_handler(IntentBuilder('DoNotDisplayIntent').require("NoKeyword").require('DisplayMoreResults').build())
    @removes_context("DisplayMoreResults")
    def handle_dont_display_more_context(self):
        pass

    @intent_handler(IntentBuilder('DisplayIntent').require("YesKeyword").require('DisplayMoreResults').build())
    def handle_display_more_context(self):
        for entry in self.delete_these_results:
            del self.all_confluence_search_results[entry]
        if len(self.all_confluence_search_results) > 0:
            self.process_url_list()


def create_skill():
    return MycroftConfluenceSearch()

