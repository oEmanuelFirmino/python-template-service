import logging


class SafeFormatter(logging.Formatter):
    def format(self, record):
        if not hasattr(record, "step"):
            record.step = "-"
        if not hasattr(record, "document_id"):
            record.document_id = "-"
        return super().format(record)


def setup_logging(level=logging.INFO):
    logger = logging.getLogger()
    logger.setLevel(level)

    handler = logging.StreamHandler()

    formatter = SafeFormatter(
        "%(asctime)s - %(levelname)s - %(name)s - %(message)s - step=%(step)s"
    )

    handler.setFormatter(formatter)

    logger.handlers.clear()
    logger.addHandler(handler)


def get_logger(name: str):
    return logging.getLogger(name)
