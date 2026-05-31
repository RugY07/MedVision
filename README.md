# MedVision AI - Futuristic Medical Diagnostics

A modern medical scan analysis application built with React, TypeScript, and Supabase. This application provides AI-powered medical scan analysis with 3D visualization and real-time diagnostics.

## Features

- **AI-Powered Analysis**: Upload medical scans (X-ray, MRI, CT, DICOM) for intelligent analysis
- **3D Visualization**: Interactive 3D organ models for enhanced diagnostics
- **Real-time Results**: Instant analysis with confidence scores and detailed findings
- **Multiple Scan Types**: Support for brain, cardiac, chest, and bone scans
- **Responsive Design**: Modern UI built with Tailwind CSS and shadcn/ui components
- **Authentication**: Secure user authentication with Supabase Auth
- **Multiple AI Providers**: Supports OpenAI GPT-4 Vision and Google Gemini for analysis
- **Demo Mode**: Works without API keys for testing and development

## Getting Started

### Prerequisites

- Node.js (v18 or higher)
- npm, yarn, pnpm, or bun

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd vision-weave-med-main
```

2. Install dependencies:
```bash
npm install
# or
yarn install
# or
pnpm install
# or
bun install
```

3. Set up environment variables:
Create a `.env` file in the root directory with the following variables:
```env
VITE_SUPABASE_URL=https://lassmjhayhgstpiskcid.supabase.co
VITE_SUPABASE_PUBLISHABLE_KEY=your_supabase_anon_key_here

# AI API Keys (choose one or both)
OPENAI_API_KEY=your_openai_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
```

**Note**: For local development, you can use the default values. The app will work with demo data and doesn't require any API keys to run.

4. Start the development server:
```bash
npm run dev
# or
yarn dev
# or
pnpm dev
# or
bun dev
```

Open [http://localhost:8080](http://localhost:8080) with your browser to see the result.

## Project Structure

```
src/
├── components/          # Reusable UI components
│   ├── ui/             # shadcn/ui components
│   └── ...             # Feature-specific components
├── pages/              # Application pages
├── integrations/       # External service integrations
│   └── supabase/       # Supabase configuration
├── hooks/              # Custom React hooks
├── lib/                # Utility functions
└── assets/             # Static assets
```

## Technologies Used

- **Frontend**: React 18, TypeScript, Vite
- **Styling**: Tailwind CSS, shadcn/ui
- **Backend**: Supabase (Database, Auth, Edge Functions)
- **3D Graphics**: Three.js, React Three Fiber
- **State Management**: TanStack Query
- **Routing**: React Router DOM

## Deployment

### Build for Production

```bash
npm run build
# or
yarn build
# or
pnpm build
# or
bun build
```

### Deploy to Vercel

1. Install Vercel CLI: `npm i -g vercel`
2. Run `vercel` in the project directory
3. Follow the prompts to deploy

### Deploy to Netlify

1. Build the project: `npm run build`
2. Deploy the `dist` folder to Netlify

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -am 'Add feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request

## License

This project is licensed under the MIT License.