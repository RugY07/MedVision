import { motion } from "framer-motion";
import { Scan, Brain, Activity } from "lucide-react";
import { Button } from "./ui/button";
import heroImage from "@/assets/hero-medical-brain.jpg";

const Hero = () => {
  return (
    <section className="relative min-h-screen flex items-center justify-center overflow-hidden pt-20">
      {/* Animated background grid */}
      <div className="absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAiIGhlaWdodD0iNDAiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PGRlZnM+PHBhdHRlcm4gaWQ9ImdyaWQiIHdpZHRoPSI0MCIgaGVpZ2h0PSI0MCIgcGF0dGVyblVuaXRzPSJ1c2VyU3BhY2VPblVzZSI+PHBhdGggZD0iTSAwIDEwIEwgNDAgMTAgTSAxMCAwIEwgMTAgNDAgTSAwIDIwIEwgNDAgMjAgTSAyMCAwIEwgMjAgNDAgTSAwIDMwIEwgNDAgMzAgTSAzMCAwIEwgMzAgNDAiIGZpbGw9Im5vbmUiIHN0cm9rZT0iaHNsKDE4OCA1MCUgMzAlIC8gMC4xKSIgc3Ryb2tlLXdpZHRoPSIxIi8+PC9wYXR0ZXJuPjwvZGVmcz48cmVjdCB3aWR0aD0iMTAwJSIgaGVpZ2h0PSIxMDAlIiBmaWxsPSJ1cmwoI2dyaWQpIi8+PC9zdmc+')] opacity-30" />
      
      {/* Radial glow effect */}
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_center,_hsl(188_100%_50%_/_0.15),_transparent_70%)]" />
      
      <div className="container mx-auto px-6 relative z-10">
        <div className="grid lg:grid-cols-2 gap-12 items-center">
          {/* Left Content */}
          <motion.div
            initial={{ opacity: 0, x: -50 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.8 }}
            className="space-y-8"
          >
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2 }}
              className="inline-flex items-center gap-2 px-4 py-2 rounded-full glass-morphism holographic-border"
            >
              <Activity className="w-4 h-4 text-medical-cyan" />
              <span className="text-sm text-foreground/80">AI-Powered Diagnostics</span>
            </motion.div>

            <motion.h1
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.3 }}
              className="text-5xl lg:text-6xl font-bold leading-tight"
            >
              <span className="text-foreground/90">Next-Generation Medical AI</span>
              <br />
              <span className="glow-text">Revolutionizing</span>
              <br />
              <span className="glow-text">Medical Diagnostics</span>
            </motion.h1>

            <motion.p
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.4 }}
              className="text-xl text-muted-foreground max-w-xl"
            >
              Immersive 3D interfaces, real-time AI analysis, and holographic visualization for the future of medical imaging and diagnostics.
            </motion.p>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.5 }}
              className="flex flex-wrap gap-4"
            >
              <Button 
                size="lg" 
                className="group relative overflow-hidden"
                onClick={() => {
                  const element = document.getElementById('scan-types');
                  if (element) element.scrollIntoView({ behavior: 'smooth' });
                }}
              >
                <span className="relative z-10 flex items-center gap-2">
                  <Scan className="w-5 h-5" />
                  Start Analysis
                </span>
                <div className="absolute inset-0 bg-gradient-to-r from-medical-cyan to-medical-purple opacity-0 group-hover:opacity-100 transition-opacity" />
              </Button>
              
              <Button 
                size="lg" 
                variant="outline" 
                className="holographic-border"
                onClick={() => {
                  const element = document.getElementById('demo');
                  if (element) element.scrollIntoView({ behavior: 'smooth' });
                }}
              >
                <Brain className="w-5 h-5 mr-2" />
                Watch Demo
              </Button>
            </motion.div>

            {/* Stats */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.6 }}
              className="grid grid-cols-2 lg:grid-cols-4 gap-8 pt-8 border-t border-border/30"
            >
              <div>
                <div className="text-3xl font-bold text-medical-cyan">2.4M+</div>
                <div className="text-sm text-muted-foreground">Scans Analyzed</div>
              </div>
              <div>
                <div className="text-3xl font-bold text-medical-cyan">99.2%</div>
                <div className="text-sm text-muted-foreground">Accuracy Rate</div>
              </div>
              <div>
                <div className="text-3xl font-bold text-medical-cyan">&lt;800ms</div>
                <div className="text-sm text-muted-foreground">Response Time</div>
              </div>
              <div>
                <div className="text-3xl font-bold text-medical-cyan">1,200+</div>
                <div className="text-sm text-muted-foreground">Medical Centers</div>
              </div>
            </motion.div>
          </motion.div>

          {/* Right Content - Hero Image */}
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 1, delay: 0.3 }}
            className="relative"
          >
            <div className="relative rounded-2xl overflow-hidden glass-morphism holographic-border animate-float">
              <img
                src={heroImage}
                alt="Medical AI Brain Scan Visualization"
                className="w-full h-auto"
              />
              {/* Scan line effect */}
              <div className="absolute inset-0 scan-line pointer-events-none" />
              
              {/* Floating diagnostic cards */}
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 1, duration: 0.5 }}
                className="absolute top-8 right-8 glass-morphism p-4 rounded-xl holographic-border"
              >
                <div className="flex items-center gap-3">
                  <div className="w-3 h-3 rounded-full bg-medical-green animate-pulse-glow" />
                  <div>
                    <div className="text-xs text-muted-foreground">Status</div>
                    <div className="text-sm font-semibold">Processing</div>
                  </div>
                </div>
              </motion.div>
            </div>

            {/* Background glow */}
            <div className="absolute -inset-4 bg-gradient-to-r from-medical-cyan/20 to-medical-purple/20 blur-3xl -z-10 animate-pulse-glow" />
          </motion.div>
        </div>
      </div>
    </section>
  );
};

export default Hero;
