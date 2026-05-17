FROM yanwk/comfyui-boot:cpu

# Copy bundled ComfyUI into the working directory
RUN cp --archive /default-comfyui-bundle/ComfyUI/. /root/ComfyUI/

WORKDIR /root/ComfyUI

ENV CLI_ARGS="--listen 0.0.0.0 --cpu"

RUN pip install --no-cache-dir --upgrade pip && \
    pip install watchdog requests httpx


# Use watchmedo to listen for changes in the custom_nodes directory.
# If a .py, .js, .css, or .html file changes, it automatically restarts main.py.
CMD watchmedo auto-restart --directory=./custom_nodes "--pattern=*.py;*.js;*.css;*.html" --recursive -- python3 main.py $CLI_ARGS