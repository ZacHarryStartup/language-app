import argparse
import os

def main(folderName, functionName):
    if not os.path.exists('.github/workflows/' + folderName):
      os.makedirs('.github/workflows/' + folderName)
    ymlFile = open('.github/workflows/' + folderName + '/' + functionName + '.yml', "w")
    ymlContent = """name: Update {lambdaFunction}
on:
  workflow_dispatch:
  push:
    branches:
      - main
    paths:
      -  lambda-functions/{directory}/{lambdaFunction}.py
env:
  functionName: {lambdaFunction}
  AWS_ACCESS_KEY_ID: ${{{{ secrets.AWS_ACCESS_KEY_ID }}}}
  AWS_SECRET_ACCESS_KEY: ${{{{ secrets.AWS_SECRET_ACCESS_KEY }}}}
  AWS_REGION: ap-southeast-2
jobs:
  updateFunction:
    runs-on: ubuntu-latest
    environment: language-app
    steps:
      - name: checkout_repo
        uses: actions/checkout@v3
      - name: test secrets
        run: |
          echo ${{{{ secrets.AWS_ACCESS_KEY_ID }}}}
      - name: configure aws credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-access-key-id: ${{{{ secrets.AWS_ACCESS_KEY_ID }}}}
          aws-secret-access-key: ${{{{ secrets.AWS_SECRET_ACCESS_KEY }}}}
          aws-region: ap-southeast-2
      - name: "Zip function"
        run: |
          cd "/lambda-functions/{directory}" \\
          zip code.zip ${{{{ env.functionName }}}}.py 
      - name: "Updated ${{{{ env.functionName }}}}"
        run: aws lambda update-function-code --function-name ${{{{ env.functionName }}}} --zip-file fileb://code.zip
""".format(directory=folderName, lambdaFunction=functionName)
    ymlFile.write(ymlContent)


def parseArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--functionName",
        required=True
    )
    parser.add_argument(
        "--folderName",
        required=True
    )
    return parser.parse_args()


if __name__ == "__main__":
    main(parseArgs().folderName, parseArgs().functionName)