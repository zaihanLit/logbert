"""
Pipelines for processing raw logs to structured data
including sampling (optional), log parsing, log sequence generation by windowing, and train test splitting
"""

from argparse import ArgumentParser
import os

from dataset import SimpleParserFactory, split_train_test, sample_raw_data


def arg_parser():
    """
    add parser parameters
    :return:
    """
    parser = ArgumentParser()
    parser.add_argument("--dataset_name", help="which dataset to use",
                        choices=["hdfs", "bgl", "tbird", "hdfs_2k", "bgl_2k"])
    parser.add_argument("--data_dir", default="~/.dataset/", metavar="DIR", help="data directory")
    parser.add_argument("--output_dir", default="~/.output/", metavar="DIR", help="output directory")

    parser.add_argument('--log_file', help="log file name")
    parser.add_argument("--sample_size", default=None, type=int, help="sample raw log")
    parser.add_argument("--sample_log_file", default=None, help="if sampling raw logs, new log file name")
    parser.add_argument("--sample_dataset_name", default=None, help="if sampling raw logs, new dataset name")

    parser.add_argument("--parser_type", default=None, help="parse type drain or spell")
    parser.add_argument("--log_format", default=None, help="log format",
                        metavar="<Date> <Time> <Pid> <Level> <Component>: <Content>")
    parser.add_argument("--regex", nargs='*', help="regex to clean log messages", default='')
    parser.add_argument("--keep_para", action='store_true', help="keep parameters in log messages after parsing")
    # spell
    parser.add_argument("--st", default=0.3, type=float, help="similarity threshold")
    parser.add_argument("--depth", default=3, type=int, help="depth of all leaf nodes")
    parser.add_argument("--max_child", default=100, type=int, help="max children in each node")
    # drain
    parser.add_argument("--tau", default=0.5, type=float,
                        help="the percentage of tokens matched to merge a log message")

    # parser.add_argument("--is_process", action='store_true', help="if split train and test data")
    parser.add_argument("--window_type", type=str, choices=["sliding", "session"], help="generating log sequence")
    parser.add_argument('--window_size', default=5, type=float, help='window size(mins)')
    parser.add_argument('--step_size', default=1, type=float, help='step size(mins)')
    parser.add_argument('--train_size', default=0.4, type=float, help="train size", metavar="float or int")

    return parser


def main():
    parser = arg_parser()
    args = parser.parse_args()

    args.output_dir = os.path.expanduser(args.output_dir)
    args.data_dir = os.path.expanduser(args.data_dir)

    # sampling raw logs
    if args.sample_size is not None:
        sample_data_dir = os.path.join(args.data_dir, args.sample_dataset_name + "/")
        if not os.path.exists(sample_data_dir):
            os.makedirs(sample_data_dir, exist_ok=True)

        sample_step_size = 10000
        log_file_path = os.path.join(args.data_dir, args.dataset_name, args.log_file)
        sample_log_path = os.path.join(sample_data_dir, args.sample_log_file)
        sample_raw_data(log_file_path, sample_log_path, args.sample_size, sample_step_size)

        args.log_file = args.sample_log_file
        args.dataset_name = args.sample_dataset_name

    args.data_dir = os.path.join(args.data_dir, args.dataset_name + "/")
    args.output_dir = os.path.join(args.output_dir, args.dataset_name + "/")

    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir, exist_ok=True)

    # parse logs
    if args.parser_type is not None:
        args.log_format = " ".join([f"<{field}>" for field in args.log_format.split(",")])
        parser = SimpleParserFactory.create_parser(args.data_dir, args.output_dir, args.parser_type, args.log_format,
                                                   args.regex, args.keep_para,
                                                   args.st, args.depth, args.max_child, args.tau)
        parser.parse(args.log_file)

    split_train_test(data_dir=args.data_dir,
                     output_dir=args.output_dir,
                     log_file=args.log_file,
                     dataset_name=args.dataset_name,
                     window_type=args.window_type,
                     window_size=args.window_size,
                     step_size=args.step_size,
                     train_size=args.train_size)


if __name__ == "__main__":
    main()
