import { motion } from "framer-motion";
import { Brain, Activity, AlertTriangle, CheckCircle2, TrendingUp } from "lucide-react";
import { Card } from "./ui/card";
import { Progress } from "./ui/progress";
import { Badge } from "./ui/badge";

interface Finding {
  id: string;
  title: string;
  severity: 'critical' | 'warning' | 'normal';
  confidence: number;
  description: string;
  location?: string;
}

interface DiagnosticResultsProps {
  findings: Finding[];
  overallConfidence: number;
  scanType: string;
  modelType?: string;
  processingTime?: number;
}

const DiagnosticResults = ({ findings, overallConfidence, scanType, modelType, processingTime }: DiagnosticResultsProps) => {
  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'critical':
        return 'text-destructive';
      case 'warning':
        return 'text-medical-amber';
      default:
        return 'text-medical-green';
    }
  };

  const getSeverityIcon = (severity: string) => {
    switch (severity) {
      case 'critical':
        return <AlertTriangle className="w-5 h-5" />;
      case 'warning':
        return <Activity className="w-5 h-5" />;
      default:
        return <CheckCircle2 className="w-5 h-5" />;
    }
  };

  return (
    <section className="py-20 px-6">
      <div className="container mx-auto max-w-6xl">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-12"
        >
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full glass-morphism holographic-border mb-4">
            <Brain className="w-4 h-4 text-medical-cyan" />
            <span className="text-sm">AI Analysis Complete</span>
          </div>
          <h2 className="text-4xl font-bold mb-4">
            <span className="glow-text">Diagnostic Results</span>
          </h2>
          <p className="text-muted-foreground text-lg">
            Scan Type: <span className="text-foreground font-semibold">{scanType}</span>
            {modelType && (
              <span className="ml-2">
                • Model: <span className="text-medical-cyan">{modelType}</span>
              </span>
            )}
            {processingTime && (
              <span className="ml-2">
                • Processed in <span className="text-medical-green">{processingTime.toFixed(2)}s</span>
              </span>
            )}
          </p>
        </motion.div>

        {/* Overall Confidence Score */}
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.2 }}
          className="mb-8"
        >
          <Card className="p-8 glass-morphism holographic-border">
            <div className="flex items-center justify-between mb-4">
              <div>
                <h3 className="text-2xl font-bold mb-2">Overall Confidence</h3>
                <p className="text-muted-foreground">AI diagnostic certainty level</p>
              </div>
              <div className="text-right">
                <div className="text-5xl font-bold text-medical-cyan glow-text">
                  {overallConfidence}%
                </div>
                <div className="flex items-center gap-2 text-medical-green mt-2">
                  <TrendingUp className="w-4 h-4" />
                  <span className="text-sm">High Accuracy</span>
                </div>
              </div>
            </div>
            <Progress value={overallConfidence} className="h-3" />
          </Card>
        </motion.div>

        {/* Findings Grid */}
        <div className="grid md:grid-cols-2 gap-6">
          {findings.map((finding, index) => (
            <motion.div
              key={finding.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.1 * index }}
            >
              <Card className="p-6 glass-morphism holographic-border h-full hover:scale-105 transition-transform duration-300">
                <div className="flex items-start justify-between mb-4">
                  <div className="flex items-center gap-3">
                    <div className={`${getSeverityColor(finding.severity)}`}>
                      {getSeverityIcon(finding.severity)}
                    </div>
                    <div>
                      <h3 className="font-semibold text-lg">{finding.title}</h3>
                      {finding.location && (
                        <p className="text-sm text-muted-foreground">
                          Location: {finding.location}
                        </p>
                      )}
                    </div>
                  </div>
                  <Badge 
                    variant="outline" 
                    className={`${getSeverityColor(finding.severity)} border-current`}
                  >
                    {finding.severity.toUpperCase()}
                  </Badge>
                </div>

                <p className="text-muted-foreground mb-4">
                  {finding.description}
                </p>

                <div>
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-sm text-muted-foreground">Confidence Level</span>
                    <span className="text-sm font-semibold">{finding.confidence}%</span>
                  </div>
                  <Progress value={finding.confidence} className="h-2" />
                </div>
              </Card>
            </motion.div>
          ))}
        </div>

        {/* Action Recommendations */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.6 }}
          className="mt-12"
        >
          <Card className="p-8 glass-morphism holographic-border">
            <h3 className="text-2xl font-bold mb-4 flex items-center gap-3">
              <Activity className="w-6 h-6 text-medical-cyan" />
              Recommended Actions
            </h3>
            <ul className="space-y-3">
              <li className="flex items-start gap-3">
                <CheckCircle2 className="w-5 h-5 text-medical-green flex-shrink-0 mt-0.5" />
                <span className="text-muted-foreground">
                  Consult with a radiologist for professional interpretation
                </span>
              </li>
              <li className="flex items-start gap-3">
                <CheckCircle2 className="w-5 h-5 text-medical-green flex-shrink-0 mt-0.5" />
                <span className="text-muted-foreground">
                  Compare with previous scans to track changes over time
                </span>
              </li>
              <li className="flex items-start gap-3">
                <CheckCircle2 className="w-5 h-5 text-medical-green flex-shrink-0 mt-0.5" />
                <span className="text-muted-foreground">
                  Schedule follow-up imaging if recommended by healthcare provider
                </span>
              </li>
            </ul>
          </Card>
        </motion.div>

        {/* Disclaimer */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.8 }}
          className="mt-8 p-4 rounded-xl glass-morphism border border-medical-amber/30"
        >
          <div className="flex gap-3">
            <AlertTriangle className="w-5 h-5 text-medical-amber flex-shrink-0 mt-0.5" />
            <div className="text-sm">
              <p className="font-semibold text-medical-amber mb-1">Medical Disclaimer</p>
              <p className="text-muted-foreground">
                This AI analysis is for informational purposes only and should not replace 
                professional medical advice. Always consult with qualified healthcare professionals 
                for diagnosis and treatment decisions.
              </p>
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  );
};

export default DiagnosticResults;
