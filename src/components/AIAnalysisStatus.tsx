import { motion } from "framer-motion";
import { CheckCircle, XCircle, Clock, Cpu } from "lucide-react";
import { Card } from "./ui/card";

const AIAnalysisStatus = () => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.3 }}
      className="space-y-6"
    >
      <Card className="p-6 glass-morphism holographic-border">
        <h3 className="text-xl font-bold mb-4 glow-text">AI Analysis Requirements</h3>
        
        <div className="grid md:grid-cols-2 gap-6">
          {/* Supported */}
          <div>
            <div className="flex items-center gap-2 mb-3">
              <CheckCircle className="w-5 h-5 text-medical-green" />
              <h4 className="font-semibold text-medical-green">Supported</h4>
            </div>
            <ul className="space-y-2 text-sm text-muted-foreground">
              <li className="flex items-start gap-2">
                <span className="text-medical-green">•</span>
                Medical X-rays, MRI, CT scans
              </li>
              <li className="flex items-start gap-2">
                <span className="text-medical-green">•</span>
                DICOM format files
              </li>
              <li className="flex items-start gap-2">
                <span className="text-medical-green">•</span>
                High-contrast medical images
              </li>
              <li className="flex items-start gap-2">
                <span className="text-medical-green">•</span>
                Grayscale anatomical scans
              </li>
            </ul>
          </div>

          {/* Not Supported */}
          <div>
            <div className="flex items-center gap-2 mb-3">
              <XCircle className="w-5 h-5 text-destructive" />
              <h4 className="font-semibold text-destructive">Not Supported</h4>
            </div>
            <ul className="space-y-2 text-sm text-muted-foreground">
              <li className="flex items-start gap-2">
                <span className="text-destructive">•</span>
                Regular photos or screenshots
              </li>
              <li className="flex items-start gap-2">
                <span className="text-destructive">•</span>
                Non-medical images
              </li>
              <li className="flex items-start gap-2">
                <span className="text-destructive">•</span>
                Low-quality or blurry images
              </li>
              <li className="flex items-start gap-2">
                <span className="text-destructive">•</span>
                Text documents or charts
              </li>
            </ul>
          </div>
        </div>

        {/* Status Info */}
        <div className="mt-6 pt-6 border-t border-border/30 grid md:grid-cols-3 gap-4">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg glass-morphism holographic-border flex items-center justify-center">
              <CheckCircle className="w-5 h-5 text-medical-cyan" />
            </div>
            <div>
              <div className="text-sm font-semibold">Current Status</div>
              <div className="text-xs text-muted-foreground">Ready for scan upload</div>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg glass-morphism holographic-border flex items-center justify-center">
              <Clock className="w-5 h-5 text-medical-cyan" />
            </div>
            <div>
              <div className="text-sm font-semibold">Processing Time</div>
              <div className="text-xs text-muted-foreground">~2.5s</div>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg glass-morphism holographic-border flex items-center justify-center">
              <Cpu className="w-5 h-5 text-medical-cyan" />
            </div>
            <div>
              <div className="text-sm font-semibold">AI Models</div>
              <div className="text-xs text-muted-foreground">Gemini 2.5 Flash</div>
            </div>
          </div>
        </div>
      </Card>

      {/* Important Notice */}
      <Card className="p-4 glass-morphism border-warning-amber/30">
        <div className="flex items-start gap-3">
          <div className="w-5 h-5 rounded-full bg-warning-amber/20 flex items-center justify-center flex-shrink-0 mt-0.5">
            <span className="text-warning-amber text-xs">!</span>
          </div>
          <div className="text-sm">
            <p className="font-semibold mb-1 text-warning-amber">AI Analysis Status</p>
            <p className="text-muted-foreground">
              Upload a medical scan to begin intelligent AI analysis. Only valid medical scans will be processed.
            </p>
          </div>
        </div>
      </Card>
    </motion.div>
  );
};

export default AIAnalysisStatus;
