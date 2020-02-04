# servo-ec2s3

_Optune adjust driver for EC2 Instance settings via S3_

This driver presently updates settings of EC2 instances using commands stored on an s3 bucket. The types of commands and supported EC2 targets are dependent on the bundled encoder.

__Note__ this driver requires `adjust.py` and `encoders/base.py` base classes from the [Optune servo core](https://github.com/opsani/servo/). They can be copied or symlinked here as part of packaging.

__Note__ An encoder class will also be required. While this driver is mostly intended for use with the [dotnet encoder class](https://github.com/kumulustech/encoder-dotnet/) (`encoders/dotnet.py`), other encoders based on the Opsani base should be compatible.

When the `describe_endpoint` is configured in config.yaml, it must point to a web endpoint populated with content that is parsable by the bundled encoder. External drivers which support `validator` configuration (such as servo-ec2win) can use the endpoint data with the validator exposed by this driver to verify the updated settings have taken effect.

When `describe_endpoint` is used with the dotnet encoder, the endpoint is expected to contain resulting json from the ps1 script produced by the `encode_describe` method of said dotnet encoder class. __Note__ as new Windows settings are added, their respective `encode_describe` methods must also be implemented in order to keep the describe.ps1 script produced by the encoder up to date. See `describe_endpoint_dotnet.ps1.example`, `describe_site.ps1.example`, and `user_data_dotnet.example` for usage

## Required IAM Permissions

All hosts that reference the config file should have an IAM role (instance profile) configured with a policy to allow read only access to the desired bucket path. For example:

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "s3:Get*",
                "s3:List*"
            ],
            "Resource": [
                "arn:aws:s3:::example-bucket.example.com/ws2012-sandbox/*",
                "arn:aws:s3:::example-bucket.example.com"
            ]
        }
    ]
}
```

As for the account provided for the servo, the permissions required are:

S3 Permissions; Applied to the adjust file in s3 to facilitate updating and parsing

- s3:PutObject
- s3:GetObject

## Installation (encoder-dotnet)

```bash
docker build -t opsani/servo-ec2s3-ab .

docker run -d --name opsani-servo \
    -v /path/to/optune_auth_token:/opt/optune/auth_token \
    -v /path/to/config.yaml:/servo/config.yaml \
    opsani/servo-ec2s3-ab --auth-token /opt/optune/auth_token --account my_account my_app
```

Where:

- `/path/to/optune_auth_token` - file containing the authentication token for the Optune backend service
- `/path/to/config.yaml` - config file containing (see above for details).
- `my_account` - your Optune account name
- `my_app` - the application name

## How to run tests

Prerequisites:

- Python 3.5 or higher
- PyTest 4.3.0 or higher

Follow these steps:

1. Pull the repository
1. Copy/symlink `adjust` (no file extension) from this repo's project folder to folder `test/`, rename to `adjust_driver.py`
1. Copy/symlink `adjust.py` from `https://github.com/opsani/servo/tree/master/` to folder `test/`
1. Copy/symlink `base.py` from `https://github.com/opsani/servo/tree/master/encoders` to folder `test/encoders/`
1. Copy/symlink `dotnet.py` from `https://github.com/kumulustech/encoder-dotnet` to folder `test/encoders/`
1. Source your aws_config.env file containing your AWS service key (or ensure your /home/user/.aws folder has a populated credentials file )
    1. The account used must have the servo permissions detailed above
1. Add a valid `config.yaml` to folder `test/` (see config.yaml.example for a reference)
1. Run `python3 -m pytest` from the test folder
