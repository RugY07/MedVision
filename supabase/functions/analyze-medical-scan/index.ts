import "https://deno.land/x/xhr@0.1.0/mod.ts";
import { serve } from "https://deno.land/std@0.168.0/http/server.ts";

const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
};

serve(async (req) => {
  if (req.method === 'OPTIONS') {
    return new Response(null, { headers: corsHeaders });
  }

  try {
    const { imageData, scanType } = await req.json();
    
    // Check if custom ML model server is available
    const ML_MODEL_SERVER_URL = Deno.env.get('ML_MODEL_SERVER_URL');
    
    // Try custom ML model first
    if (ML_MODEL_SERVER_URL) {
      console.log(`Analyzing ${scanType} scan with custom ML model...`);
      
      try {
        const mlResponse = await fetch(`${ML_MODEL_SERVER_URL}/predict`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            image_data: imageData,
            scan_type: scanType,
            confidence_threshold: 0.5
          })
        });

        if (mlResponse.ok) {
          const mlResult = await mlResponse.json();
          
          // Convert ML model output to expected format
          const findings = mlResult.predictions.map((pred: any, index: number) => ({
            id: `ml_${index}`,
            title: pred.class.replace('_', ' ').toUpperCase(),
            severity: pred.confidence > 0.8 ? "critical" : pred.confidence > 0.6 ? "warning" : "normal",
            confidence: Math.round(pred.confidence * 100),
            description: `AI model detected ${pred.class.replace('_', ' ')} with ${Math.round(pred.confidence * 100)}% confidence`,
            location: "Analyzed region"
          }));

          const analysisResult = {
            findings: findings,
            overallConfidence: Math.round(mlResult.confidence * 100),
            scanType: scanType,
            isValidMedicalScan: true,
            modelType: "custom_ml",
            processingTime: mlResult.processing_time
          };
          
          return new Response(
            JSON.stringify(analysisResult),
            { headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
          );
        }
      } catch (mlError) {
        console.log('ML model server unavailable, falling back to general AI:', mlError);
      }
    }
    
    // Fallback to general AI models
    const OPENAI_API_KEY = Deno.env.get('OPENAI_API_KEY');
    const GEMINI_API_KEY = Deno.env.get('GEMINI_API_KEY');

    console.log(`Analyzing ${scanType} scan with general AI...`);

    // System prompt for medical scan analysis
    const systemPrompt = `You are an advanced AI medical imaging analysis system. 
Analyze the provided medical scan image and return ONLY a valid JSON object with this exact structure:
{
  "findings": [
    {
      "id": "unique_id",
      "title": "Finding Title",
      "severity": "normal" | "warning" | "critical",
      "confidence": 85-99,
      "description": "Detailed description",
      "location": "Anatomical location"
    }
  ],
  "overallConfidence": 85-99,
  "scanType": "${scanType}",
  "isValidMedicalScan": true | false
}

IMPORTANT VALIDATION RULES:
- If the image is NOT a valid medical scan (X-ray, MRI, CT, DICOM), set "isValidMedicalScan": false
- Only analyze actual medical imaging: grayscale anatomical scans, DICOM files, X-rays, MRI, CT scans
- Reject: photos, screenshots, documents, charts, non-medical images
- Provide 3-5 findings for valid scans
- Use appropriate severity levels based on observations
- Confidence scores should reflect certainty (85-99%)`;

    let response;

    // Try OpenAI first
    if (OPENAI_API_KEY) {
      response = await fetch('https://api.openai.com/v1/chat/completions', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${OPENAI_API_KEY}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          model: 'gpt-4-vision-preview',
          messages: [
            { role: 'system', content: systemPrompt },
            { 
              role: 'user', 
              content: [
                {
                  type: 'text',
                  text: `Analyze this ${scanType} medical scan and return the JSON analysis.`
                },
                {
                  type: 'image_url',
                  image_url: { url: imageData }
                }
              ]
            }
          ],
          temperature: 0.3,
          max_tokens: 2000
        }),
      });
    }
    // Try Gemini as fallback
    else if (GEMINI_API_KEY) {
      response = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent?key=${GEMINI_API_KEY}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          contents: [{
            parts: [
              { text: `${systemPrompt}\n\nAnalyze this ${scanType} medical scan and return the JSON analysis.` },
              { inline_data: { mime_type: "image/jpeg", data: imageData.split(',')[1] } }
            ]
          }],
          generationConfig: {
            temperature: 0.3,
            maxOutputTokens: 2000
          }
        }),
      });
    }
    // Demo mode - return mock analysis
    else {
      console.log('No AI API keys configured, returning demo analysis');
      const demoAnalysis = {
        findings: [
          {
            id: "demo_1",
            title: "Demo Finding",
            severity: "normal",
            confidence: 95,
            description: "This is a demo analysis. Please configure ML_MODEL_SERVER_URL, OPENAI_API_KEY or GEMINI_API_KEY for real analysis.",
            location: "General area"
          }
        ],
        overallConfidence: 95,
        scanType: scanType,
        isValidMedicalScan: true,
        modelType: "demo"
      };
      
      return new Response(
        JSON.stringify(demoAnalysis),
        { headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
      );
    }

    if (!response.ok) {
      const errorText = await response.text();
      console.error('AI API error:', response.status, errorText);
      
      if (response.status === 429) {
        return new Response(
          JSON.stringify({ error: 'Rate limit exceeded. Please try again in a moment.' }),
          { status: 429, headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
        );
      }
      
      if (response.status === 401 || response.status === 403) {
        return new Response(
          JSON.stringify({ error: 'API key invalid or expired. Please check your API configuration.' }),
          { status: 401, headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
        );
      }

      throw new Error(`AI API error: ${response.status}`);
    }

    const data = await response.json();
    let content;
    
    // Handle different API response formats
    if (data.choices && data.choices[0] && data.choices[0].message) {
      // OpenAI format
      content = data.choices[0].message.content;
    } else if (data.candidates && data.candidates[0] && data.candidates[0].content) {
      // Gemini format
      content = data.candidates[0].content.parts[0].text;
    } else {
      throw new Error('Unexpected API response format');
    }
    
    console.log('AI Response:', content);

    // Parse the JSON response
    let analysisResult;
    try {
      // Extract JSON from markdown code blocks if present
      const jsonMatch = content.match(/```(?:json)?\s*(\{[\s\S]*\})\s*```/) || 
                       content.match(/(\{[\s\S]*\})/);
      
      if (jsonMatch) {
        analysisResult = JSON.parse(jsonMatch[1]);
      } else {
        analysisResult = JSON.parse(content);
      }

      // Validate the response structure
      if (!analysisResult.isValidMedicalScan) {
        return new Response(
          JSON.stringify({ 
            error: 'Invalid medical scan detected. Please upload a valid medical imaging file (X-ray, MRI, CT scan, or DICOM).',
            isValidMedicalScan: false 
          }),
          { status: 400, headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
        );
      }

      return new Response(
        JSON.stringify(analysisResult),
        { headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
      );

    } catch (parseError) {
      console.error('Failed to parse AI response:', parseError, content);
      throw new Error('Failed to parse AI analysis results');
    }

  } catch (error) {
    console.error('Analysis error:', error);
    return new Response(
      JSON.stringify({ 
        error: error instanceof Error ? error.message : 'Analysis failed',
        details: 'An error occurred during scan analysis. Please try again.'
      }),
      { status: 500, headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
    );
  }
});
