from flowlauncher import FlowLauncher
import webbrowser
import urllib.parse
import re
import pyperclip
import wordhoard
import os
import contextlib
import logging

logging.basicConfig(
    level=logging.INFO,
    filename="plugin.log",
    encoding="utf-8",
    format="[%(asctime)s] [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
wordhoard.logger.setLevel(logging.ERROR)
wordhoard.logger.propagate = False

# curl -v "http://thesaurus.altervista.org/thesaurus/v1?key=yPDjokt1NbBTcnJ2DblW&language=en_US&output=json&word=greeting"
# database = pandas.read_parquet("assets/synonyms.parquet")


def retrieve_synonyms(word):
    with open(os.devnull, "w") as f, contextlib.redirect_stdout(f):
        syns = wordhoard.Synonyms(word).find_synonyms()
    logging.info(syns)
    return [
        dict(
            Title=entry,
            SubTitle="",
            IcoPath="assets/translate.png",
            JsonRPCAction={
                "method": "Flow.Launcher.ChangeQuery",
                "parameters": [entry, True]
            },
            # JsonRPCAction={
            #     "method": "copy_synonym",
            #     "parameters": [entry]
            # },
            ContextData=[entry],
            score=0
        ) for entry in syns
    ] if syns else [
            dict(
                Title="No synonyms found",
                SubTitle="",
                IcoPath="assets/alert-triangle.png",
                JsonRPCAction=dict(),
                ContextData=["synonym not found"],
                score=0
            )
        ]


class fetch_synonyms(FlowLauncher):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.overwrite_existing = bool(self.settings.get("overwrite_existing"))

    def query(self, query):
        logging.info(query)
        if re.match(r"^[0-9A-Za-z ]+|$", query):
            word = query[:-1]
            logging.info(f"query: {word}")
            return retrieve_synonyms(word)

    def context_menu(self, data):
        return [
            dict(
                Title=data[0],
                SubTitle=f"Search for the meaning of '{data[0]}'",
                IcoPath="assets/external-link.png",
                JsonRPCAction={
                    "method": "look_up",
                    "parameters": [data[0]]
                },
                score=0
            )
        ]

    def look_up(self, word):
        webbrowser.open(url = "https://google.com/search?q=" +
                        urllib.parse.quote(f"{word} meaning"))

    def copy_synonym(self, synonym):
        pyperclip.copy(synonym)

    # def _run_query_tasks_in_parallel(self) -> List[str]:
    #     """
    #     Runs the query tasks in parallel using a ThreadPool.

    #     :return: list
    #     :rtype: nested list
    #     """
    #     tasks = [self._query_collins_dictionary, self._query_merriam_webster, self._query_synonym_com,
    #              self._query_thesaurus_com, self._query_wordnet]

    #     running_tasks = []
    #     try:
    #         for task in tasks:
    #             running_tasks.append(task())
    #         return running_tasks
    #     except Exception as error:
    #         logger.error('An unknown error occurred in the following code segment:')
    #         logger.error(''.join(traceback.format_tb(error.__traceback__)))