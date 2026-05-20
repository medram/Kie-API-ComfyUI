import { app } from "../../scripts/app.js";

app.registerExtension({
  name: "kie.settings",
  settings: [
    {
      id: "kie.api_key",
      name: "API Key",
      type: "text",
      defaultValue: "",
      category: ["Kie API", "Settings", "API Key"],
      tooltip:
        "Your kie.ai API key. Get one at https://kie.ai. " +
        "This can also be set via the KIE_API_KEY environment variable (which takes priority).",
    },
    {
      id: "kie.openrouter_api_key",
      name: "OpenRouter API Key",
      type: "text",
      defaultValue: "",
      category: ["Kie API", "Settings", "OpenRouter API Key"],
      tooltip:
        "Your OpenRouter API key. Get one at https://openrouter.ai. " +
        "This can also be set via the OPENROUTER_API_KEY environment variable (which takes priority).",
    },
  ],
});
