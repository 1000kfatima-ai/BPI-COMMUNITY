name: Build APK

on:
  push:
    branches: [ main ]
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.10'

      - name: Install dependencies
        run: |
          sudo apt-get update
          sudo apt-get install -y build-essential libffi-dev python3-dev
          pip install --upgrade pip
          pip install Cython==0.29.33

      - name: Build with Buildozer
        uses: ArtemSerebriakov/buildozer-action@v1
        with:
          buildozer_version: master
          command: buildozer android debug
          repository_root: .

      - name: Upload APK
        uses: actions/upload-artifact@v4
        with:
          name: package
          path: bin/*.apk
