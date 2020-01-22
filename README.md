# TODO

## How to run tests

Prerequisites:

* Python 3.5 or higher
* PyTest 4.3.0 or higher

Follow these steps:

1. Pull the repository
1. Copy/symlink `adjust` (no file extension) from this repo's project folder to folder `test/`, rename to `adjust_driver.py`
1. Copy/symlink `adjust.py` from `https://github.com/opsani/servo/tree/master/` to folder `test/`
1. Copy/symlink `base.py` from `https://github.com/opsani/servo/tree/master/encoders` to folder `test/encoders/`
1. Copy/symlink `dotnet.py` from `https://github.com/kumulustech/encoder-dotnet` to folder `test/encoders/`
1. Source your aws_config.env file containing your AWS service key (or ensure your /home/user/.aws folder has a populated credentials file )
1. Run `python3 -m pytest` from the test folder
