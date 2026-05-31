import { useState } from "react";
import { supabase } from "@/integrations/supabase/client";
import { useToast } from "@/hooks/use-toast";

export interface ScanFinding {
  id: string;
  title: string;
  severity: "critical" | "warning" | "normal";
  confidence: number;
  description: string;
  location?: string;
}

export interface AnalysisResults {
  findings: ScanFinding[];
  overallConfidence: number;
  scanType: string;
  isValidMedicalScan?: boolean;
  modelType?: string;
  processingTime?: number;
}

const analyzeScan = async (file: File, scanType: string): Promise<AnalysisResults> => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();

    reader.onloadend = async () => {
      const base64data = reader.result as string;

      try {
        const { data, error } = await supabase.functions.invoke("analyze-medical-scan", {
          body: {
            imageData: base64data,
            scanType: scanType,
          },
        });

        if (error) throw error;

        if (data.error) {
          reject(new Error(data.error));
          return;
        }

        if (!data.isValidMedicalScan) {
          reject(new Error("Invalid medical scan. Please upload a valid medical imaging file."));
          return;
        }

        resolve({
          ...data,
          modelType: data.modelType || "general_ai",
          processingTime: data.processingTime || 0,
        });
      } catch (err) {
        console.error("Analysis error:", err);
        reject(err);
      }
    };

    reader.onerror = () => {
      reject(new Error("Failed to read file"));
    };

    reader.readAsDataURL(file);
  });
};

export const useAnalyzeScan = (scanType: string) => {
  const [analysisResults, setAnalysisResults] = useState<AnalysisResults | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const { toast } = useToast();

  const handleFileSelect = async (file: File) => {
    setIsAnalyzing(true);
    try {
      const results = await analyzeScan(file, scanType);
      setAnalysisResults(results);
    } catch (error) {
      console.error("Analysis failed:", error);
      toast({
        title: "Analysis Failed",
        description:
          error instanceof Error ? error.message : "Failed to analyze scan. Please try again.",
        variant: "destructive",
      });
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleNewScan = () => {
    setAnalysisResults(null);
    setIsAnalyzing(false);
  };

  return {
    analysisResults,
    isAnalyzing,
    handleFileSelect,
    handleNewScan,
  };
};
