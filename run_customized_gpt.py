
from argparse import ArgumentParser
import os

from dotenv import load_dotenv
from llama_index import GPTVectorStoreIndex, StorageContext, load_index_from_storage


load_dotenv()

os.environ['OPENAI_API_KEY'] = os.getenv('OPENAIKEY')


def get_response(inputtext, query_engine):
    response = query_engine.query(inputtext)
    return response.response


def get_argparser():
    argparser = ArgumentParser(description='Run customized GPT')
    argparser.add_argument('indexdir', help='directory of customized GPT index (.json)')
    return argparser


if __name__ == '__main__':
    args = get_argparser().parse_args()
    storage_context = StorageContext.from_defaults(persist_dir=args.indexdir)
    gptindex = load_index_from_storage(storage_context)
    query_engine = gptindex.as_query_engine()

    done = False
    while not done:
        inputtext = input('Prompt> ')
        if len(inputtext.strip()) == 0:
            done = True
        else:
            reply = get_response(inputtext, query_engine)
            print(reply)
