# switchbo-pg
sandbox
## USAGE
- 環境変数ファイルを作成する `cp .env.tmpl .env`
- .env ファイルの `API_TOKEN`, `API_SECRET` をswitchbotアプリからコピーして入れる
- 依存関係のインストール `pipenv sync --dev`
- 実行する `pipenv run python main.py`

## NOTE
- API仕様などは[公式](https://github.com/OpenWonderLabs/SwitchBotAPI#get-device-list)を参考に