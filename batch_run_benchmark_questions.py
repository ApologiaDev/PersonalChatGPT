
from argparse import ArgumentParser
import os
import json
from glob import glob

import pandas as pd
from dotenv import load_dotenv
from llama_index import StorageContext, load_index_from_storage
from tqdm import tqdm


load_dotenv()

os.environ['OPENAI_API_KEY'] = os.getenv('OPENAIKEY')


def get_response(inputtext, query_engine):
    response = query_engine.query(inputtext)
    return response.response


def get_argparser():
    argparser = ArgumentParser(description='Run customized GPT')
    argparser.add_argument('indexdir', help='directory of customized GPT index (.json)')
    argparser.add_argument('outputxlsx', help='output path of the answers to benchmark questions (*.xlsx)')
    return argparser


def yield_questions(questiondir):
    for questionpath in tqdm(glob(os.path.join(questiondir, '*.json'))):
        yield questionpath, os.path.basename(questionpath)


def yield_answer(questiondir, query_engine):
    for questionpath, filename in yield_questions(questiondir):
        data = json.load(open(questionpath, 'r'))
        question = data['question']
        answer = get_response(question, query_engine)
        yield {
            'file': filename,
            'question': question,
            'answer': answer
        }


if __name__ == '__main__':
    args = get_argparser().parse_args()
    storage_context = StorageContext.from_defaults(persist_dir=args.indexdir)
    gptindex = load_index_from_storage(storage_context)
    query_engine = gptindex.as_query_engine()

    this_dir = os.path.dirname(__file__)
    all_answers = [
        item
        for item in yield_answer(os.path.join(this_dir, 'benchmark_questions'), query_engine)
    ]

    pd.DataFrame.from_records(all_answers).to_excel(args.outputxlsx, index=None)
