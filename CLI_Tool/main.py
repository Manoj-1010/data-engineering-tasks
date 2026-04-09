import shlex
import sys
from logger import DualLogger
from data_io import DataIO
from processor import DataProcessor
from cli import setup_parser

def main():
    # 1. Initialize our modular components
    logger = DualLogger()
    data_io = DataIO()
    processor = DataProcessor(logger, data_io)
    parser = setup_parser(logger)
    
    logger.log("Welcome to Datatool CLI. Type 'help' to see commands or 'exit' to quit.")
    
    # 2. Main Interactive Loop
    while True:
        try:
            user_input = input("datatool> ").strip()
            
            if not user_input:
                continue
                
            if user_input.lower() in ['exit', 'quit']:
                logger.log("Exiting datatool. Goodbye!")
                break
                
            if user_input.lower() in ['help', '?', '-h', '--help']:
                logger.log("\nAvailable Commands:")
                logger.log("  ingest <input_file>                 Read data and show metadata")
                logger.log("  validate <input_file>               Check for nulls, duplicates, etc")
                logger.log("  transform <input_file> <out_file>   Clean and save (auto-matches input file format)")
                logger.log("  help                                Show this help message")
                logger.log("  exit                                Exit the tool\n")
                continue

            args = parser.parse_args(shlex.split(user_input))

            if args.command == "ingest":
                processor.ingest(args.input_file)
            elif args.command == "validate":
                processor.validate(args.input_file)
            elif args.command == "transform":
                processor.transform(args.input_file, args.output_file)

        except ValueError:
            # Caught parser error safely
            continue
        except KeyboardInterrupt:
            logger.log("\nExiting datatool. Goodbye!")
            break
        except Exception as e:
            logger.log(f"Unexpected error: {e}")

    # 3. Clean up
    logger.close()
    sys.exit(0)

if __name__ == "__main__":
    main()
