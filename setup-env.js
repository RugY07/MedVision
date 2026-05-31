#!/usr/bin/env node

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const envContent = `# Supabase Configuration
VITE_SUPABASE_URL=https://lassmjhayhgstpiskcid.supabase.co
VITE_SUPABASE_PUBLISHABLE_KEY=your_supabase_anon_key_here

# AI API Keys (choose one or both)
# OpenAI API Key (recommended for medical analysis)
OPENAI_API_KEY=your_openai_api_key_here

# Google Gemini API Key (alternative)
GEMINI_API_KEY=your_gemini_api_key_here

# Instructions:
# 1. Replace 'your_supabase_anon_key_here' with your actual Supabase anon key
# 2. Get OpenAI API key from: https://platform.openai.com/api-keys
# 3. Get Gemini API key from: https://makersuite.google.com/app/apikey
# 4. For local development without API keys, the app will work with demo data
# 5. Lovable has been completely disconnected - no Lovable API key needed!
`;

const envPath = path.join(__dirname, '.env');

if (!fs.existsSync(envPath)) {
  fs.writeFileSync(envPath, envContent);
  console.log('✅ Created .env file with default configuration');
  console.log('📝 Please update the .env file with your actual API keys');
} else {
  console.log('⚠️  .env file already exists, skipping creation');
}

console.log('\n🔧 Lovable has been completely disconnected!');
console.log('🎯 The app now uses OpenAI or Google Gemini APIs');
console.log('💡 No API keys needed for demo mode - the app works out of the box');
console.log('\n🚀 To start the development server, run:');
console.log('   npm run dev');
console.log('\n📖 For more information, see README.md');
