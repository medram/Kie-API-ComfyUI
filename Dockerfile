FROM yanwk/comfyui-boot:cpu

WORKDIR /root/ComfyUI

ENV CLI_ARGS="--cpu"

RUN pip install --no-cache-dir --upgrade pip && \
    pip install watchdog requests httpx


# Use watchmedo to listen for changes in the custom_nodes directory.
# If a .py, .js, .css, or .html file changes, it automatically restarts main.py.
CMD watchmedo auto-restart --directory=./custom_nodes "--pattern=*.py;*.js;*.css;*.html" --recursive -- python3 main.py --listen 0.0.0.0 $CLI_ARGS