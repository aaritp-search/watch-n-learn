<div align="center">
    <img src="https://raw.githubusercontent.com/gmbrianlaw/watch-n-learn/main/logo.png" width="500">
</div>

<br>

<h1 align="center">Watch N Learn</h1>

<h2>Information (Developer)</h2>

<ul>
    <li>
        <p>
            Use 'body_to_json'
            <a href="https://git.io/JMZsk">(here)</a>
            instead of Starlette's
            <a href="https://git.io/JMG9h">'Request.json()'</a>
            (incorrect)
        </p>
    </li>
    <li>
        <p>
            Use
            <a href="https://ngrok.com">ngrok</a>
            (https) for local development
        </p>
    </li>
</ul>

<h2>Script (fetch.sh)</h2>

```sh
random=$RANDOM$RANDOM

if [ -d $random ]
then
    echo
    echo "Found '$random/'"
    echo "Rerun script"
    unset random
    echo
    return 0
fi

# Default branch: main
[ $# -eq 1 ] && branch=$1 || branch=main

directory=${branch}_watch-n-learn

rm -fr $directory

mkdir $random

echo

curl https://codeload.github.com/gmbrianlaw/watch-n-learn/legacy.zip/$branch --output $random/_.zip

ditto -kx $random/_.zip $random

rm $random/_.zip

mv $random/* $directory

rm -r $random

echo
echo "[https://github.com/gmbrianlaw/watch-n-learn/tree/$branch] -=> '$directory/'"

unset random
unset branch
unset directory

echo
```
