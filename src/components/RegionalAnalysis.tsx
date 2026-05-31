import { useState } from "react";
import { motion } from "framer-motion";
import { Card } from "./ui/card";
import { Button } from "./ui/button";
import { Languages, Volume2, Loader2 } from "lucide-react";
import { supabase } from "@/integrations/supabase/client";
import { useToast } from "@/hooks/use-toast";

interface Finding {
  title: string;
  severity: string;
  confidence: number;
  description: string;
}

interface RegionalAnalysisProps {
  findings: Finding[];
  scanType: string;
}

const RegionalAnalysis = ({ findings, scanType }: RegionalAnalysisProps) => {
  const [hindiAnalysis, setHindiAnalysis] = useState<string>("");
  const [isTranslating, setIsTranslating] = useState(false);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const { toast } = useToast();

  const translateToHindi = async () => {
    setIsTranslating(true);
    try {
      const analysisText = `Scan Type: ${scanType}\n\n${findings.map(f => 
        `${f.title}: ${f.description} (Confidence: ${f.confidence}%)`
      ).join('\n\n')}`;

      const { data, error } = await supabase.functions.invoke('translate-to-hindi', {
        body: { text: analysisText }
      });

      if (error) throw error;

      setHindiAnalysis(data.translatedText);
      toast({
        title: "Translation Complete",
        description: "Analysis translated to Hindi successfully",
      });
    } catch (error) {
      console.error('Translation error:', error);
      toast({
        title: "Translation Failed",
        description: "Could not translate to Hindi. Please try again.",
        variant: "destructive",
      });
    } finally {
      setIsTranslating(false);
    }
  };

  const speakAnalysis = () => {
    if (!hindiAnalysis) {
      toast({
        title: "No Hindi Text",
        description: "Please translate to Hindi first",
        variant: "destructive",
      });
      return;
    }

    setIsSpeaking(true);
    
    // Use Web Speech API for text-to-speech
    const utterance = new SpeechSynthesisUtterance(hindiAnalysis);
    utterance.lang = 'hi-IN';
    utterance.rate = 0.9;
    
    utterance.onend = () => {
      setIsSpeaking(false);
    };
    
    utterance.onerror = () => {
      setIsSpeaking(false);
      toast({
        title: "Speech Error",
        description: "Could not play audio. Please try again.",
        variant: "destructive",
      });
    };

    window.speechSynthesis.cancel(); // Cancel any ongoing speech
    window.speechSynthesis.speak(utterance);
  };

  return (
    <section className="py-12 px-6">
      <div className="container mx-auto max-w-4xl">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="space-y-6"
        >
          <div className="text-center mb-8">
            <h2 className="text-3xl font-bold mb-2">
              <span className="glow-text">क्षेत्रीय भाषा विश्लेषण</span>
            </h2>
            <p className="text-muted-foreground">
              Regional Language Analysis - Get your diagnosis in Hindi
            </p>
          </div>

          <Card className="p-6 glass-morphism">
            <div className="flex gap-4 mb-6">
              <Button
                onClick={translateToHindi}
                disabled={isTranslating}
                className="holographic-border flex-1"
              >
                {isTranslating ? (
                  <>
                    <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                    Translating...
                  </>
                ) : (
                  <>
                    <Languages className="w-4 h-4 mr-2" />
                    Translate to Hindi
                  </>
                )}
              </Button>

              <Button
                onClick={speakAnalysis}
                disabled={!hindiAnalysis || isSpeaking}
                variant="outline"
                className="holographic-border flex-1"
              >
                {isSpeaking ? (
                  <>
                    <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                    Speaking...
                  </>
                ) : (
                  <>
                    <Volume2 className="w-4 h-4 mr-2" />
                    Listen in Hindi
                  </>
                )}
              </Button>
            </div>

            {hindiAnalysis && (
              <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                className="p-6 rounded-xl bg-background/50 border border-medical-cyan/30"
              >
                <h3 className="text-xl font-semibold mb-4 text-medical-cyan">
                  हिंदी में विश्लेषण:
                </h3>
                <div className="text-foreground whitespace-pre-wrap leading-relaxed">
                  {hindiAnalysis}
                </div>
              </motion.div>
            )}

            {!hindiAnalysis && (
              <div className="text-center py-8 text-muted-foreground">
                <Languages className="w-12 h-12 mx-auto mb-4 opacity-50" />
                <p>Click "Translate to Hindi" to get your analysis in हिंदी</p>
              </div>
            )}
          </Card>
        </motion.div>
      </div>
    </section>
  );
};

export default RegionalAnalysis;
