import { useNavigate } from "react-router-dom";
import Navigation from "@/components/Navigation";
import ScanUploader from "@/components/ScanUploader";
import DiagnosticResults from "@/components/DiagnosticResults";
import OrganModel3D from "@/components/OrganModel3D";
import Footer from "@/components/Footer";
import RegionalAnalysis from "@/components/RegionalAnalysis";
import { Button } from "@/components/ui/button";
import { ArrowLeft } from "lucide-react";
import { motion } from "framer-motion";
import { useAnalyzeScan } from "@/hooks/useAnalyzeScan";

const CardiacScan = () => {
  const { analysisResults, isAnalyzing, handleFileSelect, handleNewScan } = useAnalyzeScan("Cardiac");
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-background">
      <Navigation />
      
      <section className="pt-32 pb-12 px-6">
        <div className="container mx-auto max-w-6xl">
          <Button
            variant="outline"
            onClick={() => navigate('/')}
            className="holographic-border mb-8"
          >
            <ArrowLeft className="w-4 h-4 mr-2" />
            Back to Home
          </Button>
          
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="text-center mb-12"
          >
            <h1 className="text-5xl font-bold mb-4">
              <span className="glow-text">Cardiac Scan Analysis</span>
            </h1>
            <p className="text-muted-foreground text-lg">
              Advanced AI diagnostics for cardiac imaging and heart scans
            </p>
          </motion.div>
        </div>
      </section>

      {!analysisResults && !isAnalyzing && (
        <ScanUploader 
          onFileSelect={handleFileSelect} 
          selectedScanType="Cardiac"
        />
      )}

      {isAnalyzing && (
        <section className="py-20 px-6">
          <div className="container mx-auto max-w-4xl">
            <motion.div
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              className="text-center"
            >
              <div className="mb-8">
                <OrganModel3D />
              </div>
              <h2 className="text-3xl font-bold mb-4 glow-text">
                Analyzing Cardiac Scan with AI
              </h2>
              <p className="text-muted-foreground text-lg">
                Running advanced neural network diagnostics...
              </p>
              <div className="mt-8 flex justify-center gap-2">
                {[0, 1, 2].map((i) => (
                  <div
                    key={i}
                    className="w-3 h-3 rounded-full bg-medical-cyan animate-pulse-glow"
                    style={{ animationDelay: `${i * 0.2}s` }}
                  />
                ))}
              </div>
            </motion.div>
          </div>
        </section>
      )}

      {analysisResults && (
        <>
          <section className="py-8 px-6">
            <div className="container mx-auto max-w-6xl">
              <Button
                variant="outline"
                onClick={handleNewScan}
                className="holographic-border"
              >
                <ArrowLeft className="w-4 h-4 mr-2" />
                New Cardiac Scan
              </Button>
            </div>
          </section>
          <DiagnosticResults
            findings={analysisResults.findings}
            overallConfidence={analysisResults.overallConfidence}
            scanType={analysisResults.scanType}
          />
          <RegionalAnalysis 
            findings={analysisResults.findings}
            scanType={analysisResults.scanType}
          />
        </>
      )}
      
      <Footer />
    </div>
  );
};

export default CardiacScan;
