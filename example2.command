DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
cd $DIR
python example2.py $*
if [ "$(uname)" == "Darwin" ]; then
  echo -n -e "]0;example2.command"
  osascript -e 'tell application "Terminal" to close (every window whose name contains "example2.command")' &
fi
