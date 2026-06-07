import express from "express";
import path from "path";
import { createServer as createViteServer } from "vite";
import { GoogleGenAI, Type } from "@google/genai";
import dotenv from "dotenv";

dotenv.config();

const app = express();
const PORT = 3000;

// Body parser
app.use(express.json());

// Lazy-loaded Gemini setup to protect against missing startup key errors
let ai: GoogleGenAI | null = null;

function getGeminiClient() {
  if (!ai) {
    const apiKey = process.env.GEMINI_API_KEY;
    if (!apiKey) {
      throw new Error("GEMINI_API_KEY environment variable is not set. Please add it via Settings > Secrets.");
    }
    ai = new GoogleGenAI({
      apiKey: apiKey,
      httpOptions: {
        headers: {
          'User-Agent': 'aistudio-build',
        },
      },
    });
  }
  return ai;
}

// Full audit strategist API endpoint
app.post("/api/audit", async (req, res) => {
  try {
    const { businessName, website, industry, description, primaryGoal, adSpend } = req.body;

    if (!businessName || !industry || !description) {
      return res.status(400).json({ error: "Please input Business Name, Industry, and a Description." });
    }

    const client = getGeminiClient();

    const systemPrompt = `You are the lead performance growth architect at TNT - an elite, tech-driven performance marketing and creative cohort that solves business-level problems.
Your trademark is "We solve the business level problems that choke scale." and "It's not just Ads. It's Core Architecture." You combine rigorous server-side tracking, GTM, CAPI, and thumb-stopping visual creatives to scale businesses.
Analyze the business details provided, and output a highly professional, Indian/global market-aware growth campaign strategy and ad copy blueprint in JSON.
Be precise, realistic, bold, and action-oriented. Refer to budget scales using ₹ (Indian Rupees), Lakhs or Crores where applicable. Describe creative formats (e.g. vertical reels, UGC, WhatsApp automation, high-retention stories) and specific hooks.`;

    const contents = `Analyze my Indian/Global brand for performance scaling:
Business Name: ${businessName}
Website/Landing Page: ${website || "Not provided"}
Industry: ${industry}
Business & Audience Profile: ${description}
Primary Scale Goal: ${primaryGoal || "Lower acquisition costs & aggressive SOV growth"}
Stated Monthly Ad Budget: ₹${adSpend || "5,00,000"}

Provide a highly professional performance marketing blueprint matching this exact structure. Organize the recommendations across major channels: Meta Ads, Google Ads, programmatic, and creative assets. Ensure the tone is extremely sharp, premium, and data-backed.`;

    const response = await client.models.generateContent({
      model: "gemini-3.5-flash",
      contents: contents,
      config: {
        systemInstruction: systemPrompt,
        responseMimeType: "application/json",
        responseSchema: {
          type: Type.OBJECT,
          properties: {
            executiveSummary: {
              type: Type.STRING,
              description: "A 2-3 sentence overview written in a bold, authoritative, nonchalant, and premium tone."
            },
            channelAllocation: {
              type: Type.OBJECT,
              properties: {
                metaPercent: { type: Type.NUMBER, description: "Budget percentage allocated to Meta Ads (0-100)" },
                googlePercent: { type: Type.NUMBER, description: "Budget percentage allocated to Google Search / Performance Max (0-100)" },
                programmaticPercent: { type: Type.NUMBER, description: "Budget percentage allocated to Programmatic Ads or native channels (0-100)" },
                creativeCROPercent: { type: Type.NUMBER, description: "Budget percentage allocated specifically to creative assets & CRO experiments (0-100)" }
              },
              required: ["metaPercent", "googlePercent", "programmaticPercent", "creativeCROPercent"]
            },
            creativeHooks: {
              type: Type.ARRAY,
              items: {
                type: Type.OBJECT,
                properties: {
                  angle: { type: Type.STRING, description: "Theme or angle name (e.g., The Silent Proof, Pain-Point Contrast)" },
                  hookText: { type: Type.STRING, description: "Primary ad copy hook written to immediately seize attention (first 3 seconds)" },
                  visualConcept: { type: Type.STRING, description: "Specific video/image concept, camera framing, or asset storyboard description" },
                  targetChannel: { type: Type.STRING, description: "Best channel for this ad (e.g., Meta Reels, TikTok, YouTube Shorts)" }
                },
                required: ["angle", "hookText", "visualConcept", "targetChannel"]
              },
              description: "3 highly optimized creative ad hooks engineered to stop the scroll."
            },
            targetPersonas: {
              type: Type.ARRAY,
              items: {
                type: Type.OBJECT,
                properties: {
                  audiencename: { type: Type.STRING, description: "Catchy persona descriptor (e.g., Tech-Wear Enthusiasts, Busy Solopreneurs)" },
                  demographicsDetailed: { type: Type.STRING, description: "Ages, geos, and direct interest targets" },
                  triggerPoints: { type: Type.STRING, description: "What makes them click — primary desire or pain point" },
                  funnelPosition: { type: Type.STRING, description: "TOF, MOF, or BOF focus" }
                },
                required: ["audiencename", "demographicsDetailed", "triggerPoints", "funnelPosition"]
              },
              description: "2 hyper-targeted digital media audience segments to deploy on Meta/Google."
            },
            actionPlanSteps: {
              type: Type.ARRAY,
              items: { type: Type.STRING },
              description: "4 concrete phases in chronological order representing TNT's custom launch roadmap."
            },
            projectedMetrics: {
              type: Type.OBJECT,
              properties: {
                ctrLowBound: { type: Type.NUMBER, description: "Estimated low CTR bounds with our setups (e.g., 2.1)" },
                ctrHighBound: { type: Type.NUMBER, description: "Estimated higher CTR bounds (e.g., 4.3)" },
                cpaImprovementPct: { type: Type.NUMBER, description: "Estimated CPA cost reduction percentage (e.g., 35)" },
                roasMultiplier: { type: Type.NUMBER, description: "Projected ROAS multiplier e.g., 3.4" }
              },
              required: ["ctrLowBound", "ctrHighBound", "cpaImprovementPct", "roasMultiplier"]
            }
          },
          required: [
            "executiveSummary",
            "channelAllocation",
            "creativeHooks",
            "targetPersonas",
            "actionPlanSteps",
            "projectedMetrics"
          ]
        }
      }
    });

    const parsedStrategy = JSON.parse(response.text || "{}");
    return res.json(parsedStrategy);

  } catch (error: any) {
    console.error("Error creating AI growth audit:", error);
    return res.status(500).json({
      error: error.message || "An unexpected error occurred during the campaign generation.",
      isMissingKey: !process.env.GEMINI_API_KEY
    });
  }
});

// Setup Vite Dev server or Serve static files
async function startServer() {
  if (process.env.NODE_ENV !== "production") {
    const vite = await createViteServer({
      server: { middlewareMode: true },
      appType: "spa",
    });
    app.use(vite.middlewares);
  } else {
    const distPath = path.join(process.cwd(), "dist");
    app.use(express.static(distPath));
    app.get("*", (req, res) => {
      res.sendFile(path.join(distPath, "index.html"));
    });
  }

  app.listen(PORT, "0.0.0.0", () => {
    console.log(`Server launched effortlessly on port ${PORT}`);
  });
}

startServer();
