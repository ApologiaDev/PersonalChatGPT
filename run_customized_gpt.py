
from argparse import ArgumentParser
import os

from dotenv import load_dotenv
from gpt_index import SimpleDirectoryReader, GPTSimpleVectorIndex, LLMPredictor, PromptHelper


load_dotenv()

os.environ['OPENAI_API_KEY'] = os.getenv('OPENAIKEY')


def get_response(inputtext, gptindex):
    response = gptindex.query(inputtext, response_mode='compact')
    return response.response


def get_argparser():
    argparser = ArgumentParser(description='Run customized GPT')
    argparser.add_argument('gptindexpath', help='path for customized GPT index (.json)')
    return argparser


if __name__ == '__main__':
    args = get_argparser().parse_args()
    gptindex = GPTSimpleVectorIndex.load_from_dist(args.gptindexpath)

    done = False
    while not done:
        inputtext = input('Prompt> ')
        if len(inputtext.strip()) == 0:
            done = True
        else:
            reply = get_response(inputtext, gptindex)
            print(reply)
