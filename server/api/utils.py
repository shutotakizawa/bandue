import time
import logging

logger = logging.getLogger(__name__)
def analyzeMethod(func):
    """
    メソッドを解析するデコレーター
        メソッドのargs, kwargs, result, 実行時間をログ上に表示する
    """
    def inner(*args, **kwargs):
        logger.debug('=====================================================================')
        logger.debug('========================This is AnalyzeMethod========================')
        logger.debug('=====================================================================')
        logger.debug('【関数名】  ====> ' + func.__name__)
        logger.debug(' ↓↓↓ 【Arguments】 ↓↓↓ ')
        logger.debug(args)
        logger.debug(' ↓↓↓ 【Keyword Aurguments】 ↓↓↓ ')
        logger.debug(kwargs)
        logger.debug(' ↓↓↓ 【実行結果】 ↓↓↓ ')
        start_time = time.time()
        res = func(*args, **kwargs)
        logger.debug(res)
        total_time = time.time() - start_time
        logger.debug('【実行時間】  ====> ' + str(total_time) + '[sec]')
        logger.debug('=====================================================================')
        logger.debug('========================AnalyzeMethod Finished========================')
        logger.debug('=====================================================================')
        return func(*args, **kwargs)
    return inner


def chunked(queryset, chunk_size=1000):
    """
    メモリに載りきらないような大量なデータを扱う時に、
    QuerySetを分割して実行するメソッド
    """

    start = 0
    while True:
        chunk = queryset[start: start + chunk_size]
        for obj in chunk:
            yield obj
        if len(chunk) < chunk_size:
            raise StopIteration
        start += chunk_size
