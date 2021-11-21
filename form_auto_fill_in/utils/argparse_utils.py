# coding: utf-8
import argparse


class KwargsParamProcessor(argparse.Action):
    """Set a new argument.

    Examples:
        >>> import argparse
        >>> from form_auto_fill_in.utils import KwargsParamProcessor
        >>> parser = argparse.ArgumentParser()
        >>> parser.add_argument("--kwargs", action=KwargsParamProcessor)
        >>> args = parser.parse_args(args=["--kwargs", "foo=a", "--kwargs", "bar=b"])
        >>> (args.kwargs, args.foo, args.bar)
        (None, 'a', 'b')

    Note:
        If you run from the command line, execute as follows::

        $ python app.py --kwargs foo=a --kwargs bar=b
    """

    def __call__(self, parser, namespace, values, option_strings=None):
        k, v = values.split("=")
        setattr(namespace, k, v)
