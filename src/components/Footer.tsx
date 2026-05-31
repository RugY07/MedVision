import { Brain, Github, Twitter, Linkedin, Mail } from "lucide-react";

const Footer = () => {
  return (
    <footer className="relative border-t border-border/30 bg-background/50 backdrop-blur-sm">
      <div className="container mx-auto px-6 py-12">
        <div className="grid md:grid-cols-4 gap-8 mb-8">
          {/* Brand */}
          <div className="space-y-4">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-medical-cyan to-medical-purple flex items-center justify-center">
                <Brain className="w-6 h-6 text-primary-foreground" />
              </div>
              <div>
                <h3 className="font-bold glow-text">MedVision AI</h3>
                <p className="text-xs text-muted-foreground">Medical Diagnostics</p>
              </div>
            </div>
            <p className="text-sm text-muted-foreground">
              Next-generation medical imaging analysis powered by advanced artificial intelligence.
            </p>
          </div>

          {/* Products */}
          <div>
            <h4 className="font-semibold mb-4">Platform</h4>
            <ul className="space-y-2 text-sm text-muted-foreground">
              <li><a href="/brain-scan" className="hover:text-foreground transition-colors">AI Diagnostics</a></li>
              <li><a href="/#technology" className="hover:text-foreground transition-colors">3D Visualization</a></li>
              <li><a href="/#features" className="hover:text-foreground transition-colors">Collaboration</a></li>
              <li><a href="/chest-scan" className="hover:text-foreground transition-colors">API Access</a></li>
            </ul>
          </div>

          {/* Resources */}
          <div>
            <h4 className="font-semibold mb-4">Resources</h4>
            <ul className="space-y-2 text-sm text-muted-foreground">
              <li><a href="https://github.com/RugY07/MedVision" className="hover:text-foreground transition-colors" target="_blank" rel="noreferrer">Documentation</a></li>
              <li><a href="/" className="hover:text-foreground transition-colors">Research Papers</a></li>
              <li><a href="/" className="hover:text-foreground transition-colors">Case Studies</a></li>
              <li><a href="mailto:support@medvision.ai" className="hover:text-foreground transition-colors">Support</a></li>
            </ul>
          </div>

          {/* Legal */}
          <div>
            <h4 className="font-semibold mb-4">Legal</h4>
            <ul className="space-y-2 text-sm text-muted-foreground">
              <li><a href="/" className="hover:text-foreground transition-colors">Privacy Policy</a></li>
              <li><a href="/" className="hover:text-foreground transition-colors">Terms of Service</a></li>
              <li><a href="/" className="hover:text-foreground transition-colors">HIPAA Compliance</a></li>
              <li><a href="/" className="hover:text-foreground transition-colors">Security</a></li>
            </ul>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="pt-8 border-t border-border/30 flex flex-col md:flex-row justify-between items-center gap-4">
          <div className="text-center md:text-left">
            <p className="text-sm text-muted-foreground mb-1">
              © 2024 MedVision AI. Revolutionizing medical diagnostics with artificial intelligence.
            </p>
            <p className="text-xs text-muted-foreground">
              Developed by <span className="text-medical-cyan font-semibold">Rugweda Yende</span>
            </p>
          </div>
          
          <div className="flex items-center gap-4">
            <a href="https://x.com" className="w-9 h-9 rounded-lg glass-morphism holographic-border flex items-center justify-center hover:scale-110 transition-transform" target="_blank" rel="noreferrer">
              <Twitter className="w-4 h-4 text-muted-foreground hover:text-foreground" />
            </a>
            <a href="https://linkedin.com" className="w-9 h-9 rounded-lg glass-morphism holographic-border flex items-center justify-center hover:scale-110 transition-transform" target="_blank" rel="noreferrer">
              <Linkedin className="w-4 h-4 text-muted-foreground hover:text-foreground" />
            </a>
            <a href="https://github.com/RugY07/MedVision" className="w-9 h-9 rounded-lg glass-morphism holographic-border flex items-center justify-center hover:scale-110 transition-transform" target="_blank" rel="noreferrer">
              <Github className="w-4 h-4 text-muted-foreground hover:text-foreground" />
            </a>
            <a href="mailto:support@medvision.ai" className="w-9 h-9 rounded-lg glass-morphism holographic-border flex items-center justify-center hover:scale-110 transition-transform">
              <Mail className="w-4 h-4 text-muted-foreground hover:text-foreground" />
            </a>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
