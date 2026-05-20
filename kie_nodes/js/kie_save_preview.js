import { app } from "../../scripts/app.js";

app.registerExtension({
  name: "kie.savePreview",

  async beforeRegisterNodeDef(nodeType, nodeData) {
    // Only apply to Kie nodes
    if (!nodeData.name.startsWith("Kie")) return;

    const origOnExecuted = nodeType.prototype.onExecuted;
    nodeType.prototype.onExecuted = function (message) {
      origOnExecuted?.apply(this, arguments);

      // Handle image previews
      if (message?.images?.length > 0) {
        this._kiePreviewImages = message.images;

        if (!this._kieSaveImageButtonAdded) {
          this._kieSaveImageButtonAdded = true;
          this.addWidget("button", "💾 Save Images", null, async () => {
            const images = this._kiePreviewImages;
            if (!images || images.length === 0) return;

            try {
              const resp = await fetch("/kie/save_image", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ images }),
              });
              const result = await resp.json();
              if (result.success && result.saved > 0) {
                console.log(
                  `[Kie] Saved ${result.saved} image(s) to output folder.`,
                );
              }
            } catch (e) {
              console.error("[Kie] Failed to save images:", e);
            }
          });
          this.setSize(this.computeSize());
        }
      }

      // Handle video previews
      if (message?.videos?.length > 0) {
        this._kiePreviewVideos = message.videos;

        if (!this._kieSaveVideoButtonAdded) {
          this._kieSaveVideoButtonAdded = true;
          this.addWidget("button", "💾 Save Videos", null, async () => {
            const videos = this._kiePreviewVideos;
            if (!videos || videos.length === 0) return;

            try {
              const resp = await fetch("/kie/save_image", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ images: videos }),
              });
              const result = await resp.json();
              if (result.success && result.saved > 0) {
                console.log(
                  `[Kie] Saved ${result.saved} video(s) to output folder.`,
                );
              }
            } catch (e) {
              console.error("[Kie] Failed to save videos:", e);
            }
          });
          this.setSize(this.computeSize());
        }
      }
    };
  },
});
