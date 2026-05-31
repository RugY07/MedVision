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
    const { text } = await req.json();

    if (!text) {
      throw new Error('No text provided');
    }

    // Try OpenAI API first, then fallback to demo mode
    const OPENAI_API_KEY = Deno.env.get('OPENAI_API_KEY');
    const GEMINI_API_KEY = Deno.env.get('GEMINI_API_KEY');

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
          model: 'gpt-4',
          messages: [
            {
              role: 'system',
              content: 'You are a medical translator. Translate the following medical analysis from English to Hindi. Maintain medical terminology accuracy while making it understandable for Hindi-speaking patients. Keep the format clean and readable.'
            },
            {
              role: 'user',
              content: text
            }
          ],
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
            parts: [{
              text: `You are a medical translator. Translate the following medical analysis from English to Hindi. Maintain medical terminology accuracy while making it understandable for Hindi-speaking patients. Keep the format clean and readable.\n\n${text}`
            }]
          }],
          generationConfig: {
            temperature: 0.3
          }
        }),
      });
    }
    // Demo mode - return mock translation
    else {
      console.log('No AI API keys configured, returning demo translation');
      const demoTranslation = `${text}\n\n[Demo Hindi Translation: यह एक डेमो अनुवाद है। कृपया वास्तविक अनुवाद के लिए OPENAI_API_KEY या GEMINI_API_KEY कॉन्फ़िगर करें।]`;
      
      return new Response(
        JSON.stringify({ translatedText: demoTranslation }),
        { headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
      );
    }

    if (!response.ok) {
      const errorText = await response.text();
      console.error('AI API Error:', errorText);
      
      if (response.status === 401 || response.status === 403) {
        return new Response(
          JSON.stringify({ error: 'API key invalid or expired. Please check your API configuration.' }),
          { status: 401, headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
        );
      }
      
      throw new Error(`AI API error: ${response.status}`);
    }

    const data = await response.json();
    let translatedText;
    
    // Handle different API response formats
    if (data.choices && data.choices[0] && data.choices[0].message) {
      // OpenAI format
      translatedText = data.choices[0].message.content;
    } else if (data.candidates && data.candidates[0] && data.candidates[0].content) {
      // Gemini format
      translatedText = data.candidates[0].content.parts[0].text;
    } else {
      throw new Error('Unexpected API response format');
    }

    return new Response(
      JSON.stringify({ translatedText }),
      {
        headers: { ...corsHeaders, 'Content-Type': 'application/json' },
      }
    );

  } catch (error) {
    console.error('Translation error:', error);
    return new Response(
      JSON.stringify({ error: error instanceof Error ? error.message : 'Translation failed' }),
      {
        status: 500,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' },
      }
    );
  }
});
