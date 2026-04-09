import argparse

class InteractiveParser(argparse.ArgumentParser):
    """Custom parser that prevents exiting the interactive loop on errors."""
    
    def __init__(self, *args, **kwargs):
        # Safely extract the logger from kwargs. 
        # If argparse doesn't provide it, it defaults to None.
        self.logger = kwargs.pop('logger', None)
        super().__init__(*args, **kwargs)

    def error(self, message):
        # Use the logger if it exists, otherwise fall back to standard print
        if self.logger:
            self.logger.log(f"Error: {message}\nType 'help' for usage.")
        else:
            print(f"Error: {message}\nType 'help' for usage.")
        raise ValueError("Argparse Error")


def setup_parser(logger):
    """Configures the argparse subcommands."""
    parser = InteractiveParser(logger=logger, prog="datatool", add_help=False)
    subparsers = parser.add_subparsers(dest="command")

    # We now pass 'logger=logger' to each subparser so they have access to it
    
    # Ingest Command
    ingest_parser = subparsers.add_parser("ingest", logger=logger)
    ingest_parser.add_argument("input_file")

    # Validate Command
    validate_parser = subparsers.add_parser("validate", logger=logger)
    validate_parser.add_argument("input_file")

    # Transform Command
    transform_parser = subparsers.add_parser("transform", logger=logger)
    transform_parser.add_argument("input_file")
    transform_parser.add_argument("output_file")

    return parser