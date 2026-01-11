# PyPI Metadata Boost

Automated PyPI metadata pinging to increase download metrics for Python packages.

## 📁 Project Structure

```
pypi_boost/
├── .github/
│   └── workflows/
│       └── boost.yml          # GitHub Actions workflow
├── boost.py                   # Main automation script
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## 🚀 Features

- **Threaded Requests**: Uses 10 concurrent threads to perform 100 requests per execution
- **User-Agent Rotation**: Rotates between 10 different common pip User-Agent strings
- **Error Handling**: Comprehensive error handling to prevent workflow failures
- **Rate Limit Protection**: Built-in delays and timeout handling
- **Automated Scheduling**: Runs every hour via GitHub Actions
- **Manual Trigger**: Can be triggered manually via workflow_dispatch

## 🔧 Setup

### 1. Configure Package Name

Edit `boost.py` and update the `PACKAGE_NAME` variable:

```python
PACKAGE_NAME = "your-package-name"  # Replace with your PyPI package name
```

### 2. Install Dependencies (Local Testing)

```bash
pip install -r requirements.txt
```

### 3. Run Locally

```bash
python boost.py
```

## ⚙️ GitHub Actions Configuration

The workflow is configured to:

- **Schedule**: Run every hour (`0 * * * *`)
- **Manual Trigger**: Available via the "Actions" tab → "Run workflow"
- **Platform**: Ubuntu Latest
- **Python Version**: 3.11
- **Error Handling**: Uses `continue-on-error: true` to prevent failures

### Manual Trigger Steps:

1. Go to your repository on GitHub
2. Click on the "Actions" tab
3. Select "PyPI Metadata Boost" workflow
4. Click "Run workflow" button
5. Select branch and click "Run workflow"

## 📊 Script Behavior

- **Total Requests**: 100 per execution
- **Concurrent Threads**: 10
- **User-Agent Rotation**: 10 different pip user agents
- **Request Timeout**: 10 seconds
- **Delay Between Requests**: Random 0.1-0.5 seconds
- **Target**: PyPI JSON API endpoint

## 🛡️ Error Handling

The script handles:

- Network timeouts
- HTTP errors (rate limiting, server errors)
- Connection failures
- Unexpected exceptions

All errors are logged but don't stop execution, ensuring the GitHub Action completes successfully.

## ⚠️ Disclaimer

This tool is for educational purposes. Please review PyPI's Terms of Service and use responsibly. Excessive requests may result in rate limiting or IP blocking.

## 📝 License

MIT License - See repository for details

## 👤 Author

GitHub: [@AroopGit](https://github.com/AroopGit)
